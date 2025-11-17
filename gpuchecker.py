import torch

print("CUDA available:", torch.cuda.is_available())
print("Number of GPUs:", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(torch.cuda.get_device_name(i))
    print("Memory allocated:", torch.cuda.memory_allocated(i)/1e9, "GB")
    print("Memory reserved:", torch.cuda.memory_reserved(i)/1e9, "GB")