import openai
import os
import hashlib
import argparse
import yaml

openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text, source_language="de", target_language="en"):
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Übersetze Markdown-Text von {source_language} nach {target_language}. Das Ergebnis muss wieder gültiges Markdown sein. Sinn und Inhalt dürfen nicht verändert werden. Textbereiche und einzelne Wörter, die in Markdown als Code formatiert sind, müssen unverändert übernommen werden. Das gleiche gilt für Hyperlinks. Füge nichts hinzu und lasse nichts weg."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

def calculate_checksum(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_existing_checksum(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
            if content.startswith('---'):
                header, _ = content.split('---', 2)[1:3]
                header_data = yaml.safe_load(header)
                return header_data.get('checksum')
    except FileNotFoundError:
        return None

def load_existing_header(content):
    if content.startswith('---'):
        header, content = content.split('---', 2)[1:3]
        return yaml.safe_load(header), content
    return {}, content

def translate_markdown_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    existing_header, content = load_existing_header(content)
    new_checksum = calculate_checksum(content)
    existing_checksum = load_existing_checksum(output_file)

    if new_checksum == existing_checksum:
        print(f"No changes detected in {input_file}. Translation is not required.")
        return

    translated_content = translate_text(content)

    existing_header['checksum'] = new_checksum
    header_str = yaml.dump(existing_header, default_flow_style=False)
    final_content = f"---\n{header_str}---\n\n{translated_content}"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(final_content)
    
    print(f"Translated {input_file} and saved to {output_file}.")

def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                input_file = os.path.join(root, file)
                output_subdir = os.path.join(output_dir, os.path.relpath(root, input_dir))
                os.makedirs(output_subdir, exist_ok=True)
                output_file = os.path.join(output_subdir, file)
                translate_markdown_file(input_file, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate all Markdown files in a directory from German to English.')
    parser.add_argument('input_dir', type=str, help='Path to the input directory')
    parser.add_argument('output_dir', type=str, help='Path to the output directory')

    args = parser.parse_args()

    process_directory(args.input_dir, args.output_dir)
