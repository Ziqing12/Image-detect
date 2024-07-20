import requests
import csv

# Replace with your Azure Computer Vision API credentials
subscription_key = '878f410cae664650a3b5c32d6b006ad6' #u can replace with your own azure subscription_key
endpoint = 'https://imaged.cognitiveservices.azure.com/' #this one is mine and it is free, so the requests number is limited
ocr_url = endpoint + 'vision/v3.2/ocr'

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Azure Computer Vision API.
    Args:
        image_path (str): The path to the image file.
    Returns:
        str: The extracted text.
    """
    # Read image file
    with open(image_path, 'rb') as image:
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'
        }
        response = requests.post(ocr_url, headers=headers, data=image)
        response.raise_for_status()

        # Extract text from the response
        analysis = response.json()
        extracted_text = ""
        for region in analysis.get('regions', []):
            for line in region.get('lines', []):
                for word in line.get('words', []):
                    extracted_text += word.get('text', '') + ' '
                extracted_text += '\n'
        
    return extracted_text.strip()

def save_text_to_csv(text, csv_path):
    """
    Saves extracted text to a CSV file.

    Args:
        text (str): The text to save.
        csv_path (str): The path to the CSV file.
    """
    # Split the text into lines
    lines = text.split('\n')
    
    # Write text to CSV
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for line in lines:
            writer.writerow([line])

def main():
    # Path to the image file
    image_path = r"E:\ocr\image example\desktop-How To Read Your Prescription.png"  # Replace with the actual path to your image file
    
    # Path to the CSV file
    csv_path = r"E:\ocr\image example\new Microsoft Excel Worksheet.csv"  # Path where you want to save the CSV file

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    
    # Save the extracted text to a CSV file
    save_text_to_csv(extracted_text, csv_path)

    print(f"Extracted text saved to {csv_path}")

