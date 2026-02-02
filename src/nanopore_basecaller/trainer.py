"""
Training module for the nanopore basecaller model.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
import os


class Trainer:
    """
    Trainer class for the nanopore basecaller model.
    """
    
    def __init__(
        self,
        model,
        train_dataset,
        val_dataset=None,
        batch_size=32,
        learning_rate=1e-3,
        device=None
    ):
        """
        Initialize trainer.
        
        Args:
            model: The neural network model
            train_dataset: Training dataset
            val_dataset: Validation dataset (optional)
            batch_size (int): Batch size for training
            learning_rate (float): Learning rate
            device: Device to train on (cuda/cpu)
        """
        self.model = model
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset
        self.batch_size = batch_size
        
        # Set device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
            
        self.model.to(self.device)
        
        # CTC Loss for sequence-to-sequence learning
        self.criterion = nn.CTCLoss(blank=4, zero_infinity=True)
        
        # Optimizer
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=learning_rate
        )
        
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            factor=0.5,
            patience=5
        )
        
        self.history = {
            'train_loss': [],
            'val_loss': []
        }
        
    def train_epoch(self, dataloader):
        """
        Train for one epoch.
        
        Args:
            dataloader: DataLoader for training data
            
        Returns:
            float: Average training loss
        """
        self.model.train()
        total_loss = 0
        num_batches = 0
        
        pbar = tqdm(dataloader, desc='Training')
        for batch in pbar:
            # Move data to device
            signals = batch['signal'].to(self.device)
            sequences = batch['sequences']
            signal_lengths = batch['signal_lengths']
            seq_lengths = batch['seq_lengths']
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(signals)
            
            # Transpose for CTC: (time, batch, classes)
            outputs = outputs.transpose(0, 1)
            
            # Concatenate target sequences
            targets = torch.cat(sequences)
            
            # Calculate CTC loss
            loss = self.criterion(
                outputs,
                targets,
                signal_lengths,
                seq_lengths
            )
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=5.0)
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
            
            pbar.set_postfix({'loss': loss.item()})
        
        avg_loss = total_loss / num_batches
        return avg_loss
    
    def validate(self, dataloader):
        """
        Validate the model.
        
        Args:
            dataloader: DataLoader for validation data
            
        Returns:
            float: Average validation loss
        """
        self.model.eval()
        total_loss = 0
        num_batches = 0
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc='Validation'):
                signals = batch['signal'].to(self.device)
                sequences = batch['sequences']
                signal_lengths = batch['signal_lengths']
                seq_lengths = batch['seq_lengths']
                
                # Forward pass
                outputs = self.model(signals)
                outputs = outputs.transpose(0, 1)
                targets = torch.cat(sequences)
                
                # Calculate loss
                loss = self.criterion(
                    outputs,
                    targets,
                    signal_lengths,
                    seq_lengths
                )
                
                total_loss += loss.item()
                num_batches += 1
        
        avg_loss = total_loss / num_batches
        return avg_loss
    
    def train(self, num_epochs, save_dir='models'):
        """
        Train the model for multiple epochs.
        
        Args:
            num_epochs (int): Number of epochs to train
            save_dir (str): Directory to save model checkpoints
        """
        os.makedirs(save_dir, exist_ok=True)
        
        from .data_processor import collate_fn
        
        train_loader = DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            collate_fn=collate_fn
        )
        
        val_loader = None
        if self.val_dataset is not None:
            val_loader = DataLoader(
                self.val_dataset,
                batch_size=self.batch_size,
                shuffle=False,
                collate_fn=collate_fn
            )
        
        best_val_loss = float('inf')
        
        for epoch in range(num_epochs):
            print(f'\nEpoch {epoch+1}/{num_epochs}')
            
            # Train
            train_loss = self.train_epoch(train_loader)
            self.history['train_loss'].append(train_loss)
            print(f'Training Loss: {train_loss:.4f}')
            
            # Validate
            if val_loader is not None:
                val_loss = self.validate(val_loader)
                self.history['val_loss'].append(val_loss)
                print(f'Validation Loss: {val_loss:.4f}')
                
                # Update learning rate
                self.scheduler.step(val_loss)
                
                # Save best model
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    self.save_checkpoint(
                        os.path.join(save_dir, 'best_model.pth'),
                        epoch,
                        val_loss
                    )
                    print(f'Saved best model with validation loss: {val_loss:.4f}')
            
            # Save checkpoint every 10 epochs
            if (epoch + 1) % 10 == 0:
                self.save_checkpoint(
                    os.path.join(save_dir, f'checkpoint_epoch_{epoch+1}.pth'),
                    epoch,
                    train_loss
                )
    
    def save_checkpoint(self, path, epoch, loss):
        """
        Save model checkpoint.
        
        Args:
            path (str): Path to save checkpoint
            epoch (int): Current epoch
            loss (float): Current loss
        """
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': loss,
            'history': self.history
        }, path)
    
    def load_checkpoint(self, path):
        """
        Load model checkpoint.
        
        Args:
            path (str): Path to checkpoint file
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.history = checkpoint.get('history', self.history)
        print(f"Loaded checkpoint from epoch {checkpoint['epoch']}")
