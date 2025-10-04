#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any

class ElDebateProcessor:
    def __init__(self, data_dir: str = "/Users/maria/Desktop/EL DEBATE TXT"):
        self.data_dir = data_dir
        self.articles = []
        
    def extract_date_from_filename(self, filename: str) -> str:
        """Extract year from filename like 'El_Debate_textos_1881.txt'"""
        match = re.search(r'(\d{4})', filename)
        return match.group(1) if match else "unknown"
    
    def process_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Process a single text file and extract articles"""
        filename = os.path.basename(filepath)
        year = self.extract_date_from_filename(filename)
        
        articles = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Process each line as a separate article
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                    
                # Each line is an article
                articles.append({
                    'id': f"{year}_{i}",
                    'year': year,
                    'article_number': i,
                    'content': line,
                    'source_file': filename,
                    'date': year,  # We only have year information
                    'type': self.classify_content(line)
                })
                
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            
        return articles
    
    def classify_content(self, content: str) -> str:
        """Classify content type based on keywords"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['teatro', 'teatros', 'función', 'drama', 'comedia', 'zarzuela']):
            return 'teatro'
        elif any(keyword in content_lower for keyword in ['concierto', 'música', 'musical', 'orquesta', 'banda']):
            return 'música'
        elif any(keyword in content_lower for keyword in ['iglesia', 'misa', 'novena', 'sermón', 'parroquia']):
            return 'religioso'
        elif any(keyword in content_lower for keyword in ['circo', 'price', 'espectáculo', 'baile']):
            return 'espectáculo'
        else:
            return 'general'
    
    def process_all_files(self) -> List[Dict[str, Any]]:
        """Process all text files in the directory"""
        all_articles = []
        
        if not os.path.exists(self.data_dir):
            print(f"Directory {self.data_dir} does not exist")
            return all_articles
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.txt') and 'El_Debate_textos' in filename:
                filepath = os.path.join(self.data_dir, filename)
                print(f"Processing {filename}...")
                articles = self.process_file(filepath)
                all_articles.extend(articles)
                print(f"Found {len(articles)} articles in {filename}")
        
        return all_articles
    
    def generate_statistics(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics for the processed articles"""
        stats = {
            'total_articles': len(articles),
            'years': {},
            'types': {},
            'files_processed': set()
        }
        
        for article in articles:
            year = article['year']
            article_type = article['type']
            source_file = article['source_file']
            
            stats['years'][year] = stats['years'].get(year, 0) + 1
            stats['types'][article_type] = stats['types'].get(article_type, 0) + 1
            stats['files_processed'].add(source_file)
        
        stats['files_processed'] = list(stats['files_processed'])
        return stats
    
    def save_to_json(self, articles: List[Dict[str, Any]], output_file: str = "el_debate_data.json"):
        """Save processed articles to JSON file"""
        stats = self.generate_statistics(articles)
        
        output_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'source_directory': self.data_dir,
                'statistics': stats
            },
            'articles': articles
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to {output_file}")
        print(f"Statistics: {stats}")
        
        return output_file

def main():
    """Main function to process EL DEBATE files"""
    processor = ElDebateProcessor()
    
    print("Starting EL DEBATE text processing...")
    articles = processor.process_all_files()
    
    if articles:
        output_file = processor.save_to_json(articles)
        print(f"\nProcessing complete! Generated {len(articles)} articles")
        print(f"Data saved to: {output_file}")
    else:
        print("No articles found to process")

if __name__ == "__main__":
    main()