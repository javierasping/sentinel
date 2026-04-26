
import os
import re

def find_broken_links(root_dir):
    broken_links = []
    all_files = []
    
    # Collect all markdown files to check against
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                all_files.append(os.path.relpath(os.path.join(root, file), root_dir))

    # Regex for markdown links [text](url)
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = link_pattern.findall(content)
                    for link in links:
                        # Skip external links
                        if link.startswith(('http://', 'https://', '#', 'mailto:')):
                            continue
                        
                        # Hugo links can be relative or absolute from /content/
                        # We try to normalize them
                        normalized_link = link.lstrip('/')
                        if normalized_link.startswith('content/'):
                            normalized_link = normalized_link[8:]
                        
                        # Remove .md extension for check if it's a Hugo ref
                        check_path = normalized_link
                        if not any(all_files.count(check_path) > 0 for check_path in [normalized_link, normalized_link + '.md']):
                            # Try to see if it's a directory index
                            if not any(all_files.count(p) > 0 for p in [os.path.join(normalized_link, '_index.md'), os.path.join(normalized_link, 'index.md')]):
                                broken_links.append((file_path, link))
    
    return broken_links

if __name__ == "__main__":
    root = "/home/javiercruces/github/sentinel/content"
    broken = find_broken_links(root)
    for src, link in broken:
        print(f"{src} -> {link}")
