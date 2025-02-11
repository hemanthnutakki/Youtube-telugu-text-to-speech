import torch
import torch.nn.functional as F


def resize_or_pad(self, mel_spec, target_size):
    # Ensure the mel_spec is 2D and reshape it to 4D (batch_size, channels, height, width) for interpolation
    if mel_spec.dim() == 2:
        mel_spec = mel_spec.unsqueeze(0).unsqueeze(0)  # Shape becomes (1, 1, H, W)

    # Now mel_spec has shape (1, 1, frequency_bins, time_steps)
    # Resize using bilinear interpolation (for 2D data like spectrogram)
    mel_spec = F.interpolate(mel_spec, size=target_size, mode='bilinear', align_corners=False)

    # Return the resized mel spectrogram, removing the extra dimensions
    return mel_spec.squeeze(0).squeeze(0)  # Shape becomes (frequency_bins, time_steps)
