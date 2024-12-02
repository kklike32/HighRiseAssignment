import json

# Load the JSON data
with open('data/rag_processed_faq_data.json', 'r') as file:  # Replace 'data.json' with the name of your JSON file
    data = json.load(file)

# Function to calculate word count
def word_count(content):
    return len(content.split())

# Calculate word count for each entry
for entry in data:
    entry['word_count'] = word_count(entry['content'])

# Sort the data by word count
sorted_data = sorted(data, key=lambda x: x['word_count'])

# Get the smallest and largest 10 entries
smallest_10 = sorted_data[:10]
largest_10 = sorted_data[-10:]

# Printing average word count
total_word_count = sum(entry['word_count'] for entry in data)
average_word_count = total_word_count / len(data)
print(f"Average Word Count: {average_word_count}")

# Printing median word count
median_word_count = sorted_data[len(sorted_data) // 2]['word_count']
print(f"Median Word Count: {median_word_count}")

# Print results
print("Smallest 10 Entries (by word count):")
for entry in smallest_10:
    print(f"ID: {entry['id']}, Title: {entry['title']}, Word Count: {entry['word_count']}")

print("\nLargest 10 Entries (by word count):")
for entry in largest_10:
    print(f"ID: {entry['id']}, Title: {entry['title']}, Word Count: {entry['word_count']}")
