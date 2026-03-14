import re 
from importlib.metadata import version
import tiktoken
import torch
from torch.utils.data import Dataset, DataLoader

with open("verdict.txt", "r", encoding="utf-8") as f:
  raw_text = f.read()
    
# print("Total number of character:", len(raw_text))
# print(raw_text[:99])

text = "Hello, world. This, is a test."
result = re.split(r'(\s)', text)

# print(result)

result = re.split(r'([,.]|\s)', text)
# print(result)

result = [item.strip() for item in result if item.strip()]
# print(result)

text = "Hello, world. Is this-- a test?"
result = re.split(r'([,.?_!"()\']|--|\s)', text)
result = [item.strip() for item in result if item.strip()]
# print(result)


preprocessed = re.split(r'([,.?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
# print(len(preprocessed))

# print(preprocessed[:30])

all_words = sorted(list(set(preprocessed)))
vocab_size = len(all_words)
# print(vocab_size)

# Creating a vocabulary
vocab = {token:integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    # print(item)
    if i > 50:
        break
     

# Tokenizer
class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i:s for s,i in vocab.items()}
    
    def encode(self, text):
        preprocessed = re.split(r'([,.?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
        
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids]) 
        
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text

tokenizer = SimpleTokenizerV1(vocab)
 
text = """"It's the last he painted, you know," Mrs. Gisburn said with pardonable pride."""
ids = tokenizer.encode(text)
# print(ids)

# print("---------------")
# print(tokenizer.decode(ids))
tokenizer.decode(tokenizer.encode(text))


all_tokens = sorted(list(set(preprocessed)))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
vocab = {token:integer for integer,token in enumerate(all_tokens)}
 
# print(len(vocab.items()))

for i, item in enumerate(list(vocab.items())[-5:]):
    print(item)

# Adjust tokenizer from code listing
class SimpleTokenizerV2: 
    def __init__(self, vocab): 
        self.str_to_int = vocab 
        self.int_to_str = { i:s for s,i in vocab.items()} 

    def encode(self, text): 
        preprocessed = re.split(r'([,.?_!"()\']|--|\s)', text) 
        preprocessed = [item.strip() for item in preprocessed if item.strip()] 
        preprocessed = [item if item in self.str_to_int else 
                        "<|unk|>" for item in preprocessed] 
        
        ids = [self.str_to_int[s] for s in preprocessed] 
        return ids 

    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
 
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text

text1 = 'Hello, do you like pap?'
text2 = 'In the persian kingdom'
text = " <|endoftext|> ".join((text1, text2)) 
# print(text)

tokenizer = SimpleTokenizerV2(vocab)
# print(tokenizer.encode(text))
# print(tokenizer.decode(tokenizer.encode(text)))

# Using BPE tokenizer
# print("tiktoken version:", version("tiktoken"))
tokenizer = tiktoken.get_encoding("gpt2")
text = "Hello, do you like tea? <|endoftext|> In the sunlit terraces of someunknownPlace." 
integers = tokenizer.encode(text, allowed_special={"<|endoftext|>"}) 
# print(integers)
# print(tokenizer.decode(integers))


# BFE tokenizer on unknown words "Akwirw ier"
tokenizer = tiktoken.get_encoding("gpt2")
text = "Akwirw ier"
integers = tokenizer.encode(text)
# print(integers)
# print(tokenizer.decode(integers))

# Implementing a data loader
with open("verdict.txt", "r", encoding="utf-8") as file:
    content = file.read()
enc_content = tokenizer.encode(content)
# print(len(enc_content))
# print(len(tokenizer.decode(enc_content)))

# Remove the first 50 tokens from the dataset 
enc_sample = enc_content[50:]
context_size = 6
x = enc_sample[:context_size]
y = enc_sample[1:context_size+1]
print(f"x: {x}") 
print(f"y: {y}")

# Create the next-word prdiction tasks
for i in range (1, context_size+1):
    context = enc_sample[:i]
    desired = enc_sample[i]
    print(tokenizer.decode(context), "----->", tokenizer.decode([desired]))
    
# A  dataser for batched inputs and targets
class GPTDatasetV1(Dataset):
    def __init__(self, txt, tokenizer, max_length, stride):
        self.tokenizer = tokenizer
        self.input_ids = []
        self.target_ids = []

        token_ids = tokenizer.encode(txt)
        for i in range(0, len(token_ids) - max_length, stride): 
            input_chunk = token_ids[i:i + max_length] 
            target_chunk = token_ids[i + 1: i + max_length + 1] 
            self.input_ids.append(torch.tensor(input_chunk)) 
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]
    
    # A data loader to generate batches with input-with pairs
    def create_dataloader_v1(txt, batch_size=4, max_length=256, stride=128, shuffle=True, drop_last=True): 
        tokenizer = tiktoken.get_encoding("gpt2") 
        dataset = GPTDatasetV1(txt, tokenizer, max_length, stride) 
        dataloader = DataLoader( dataset, batch_size=batch_size, shuffle=shuffle, drop_last=drop_last) 
        return dataloader
    
    with open("verdict.txt", "r", encoding="utf-8") as filee:
        raw_text2 = filee.read()

    dataloader = create_dataloader_v1(raw_text2, batch_size=1, max_length=4, stride=1, shuffle=False)

    data_iter = iter(dataloader)
    first_batch = next(data_iter)
    print(first_batch)
