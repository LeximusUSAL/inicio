#!/usr/bin/env python3
"""
Comprehensive Musical Magazines Analyzer
Analyzes all 19 Spanish music magazines from 1842-2024
Provides exact dates, word counts, and detailed musical lexicon analysis
"""

import os
import re
import json
import glob
from collections import Counter, defaultdict
from datetime import datetime
# import pandas as pd  # Not needed

class ComprehensiveMusicalMagazinesAnalyzer:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.magazines_data = {}
        self.total_files = 0
        self.total_words = 0
        
        # Musical vocabulary categories
        self.musical_genres = [
            'ópera', 'opera', 'concierto', 'sinfonía', 'sinfonia', 'cámara', 'camara',
            'jazz', 'rock', 'pop', 'electrónica', 'electronica', 'indie', 'clásica', 'clasica',
            'flamenco', 'zarzuela', 'opereta', 'ballet', 'danza', 'coral', 'oratorio',
            'cantata', 'misa', 'réquiem', 'requiem', 'suite', 'sonata', 'cuarteto',
            'quinteto', 'trío', 'trio', 'dúo', 'duo', 'solo', 'folclórica', 'folclorica',
            'tradicional', 'popular', 'culta', 'ligera', 'sacra', 'religiosa'
        ]
        
        self.instruments = [
            'piano', 'guitarra', 'violín', 'violin', 'viola', 'violonchelo', 'violoncelo',
            'contrabajo', 'flauta', 'oboe', 'clarinete', 'fagot', 'trompa', 'trompeta',
            'trombón', 'trombon', 'tuba', 'timpani', 'percusión', 'percusion',
            'arpa', 'órgano', 'organo', 'clavicémbalo', 'clavicembalo', 'bandurria',
            'laúd', 'laud', 'castañuelas', 'castanuelas', 'tambor', 'batería', 'bateria',
            'saxofón', 'saxofon', 'acordeón', 'acordeon', 'harmónica', 'harmonica'
        ]
        
        self.technical_terms = [
            'armonía', 'armonia', 'ritmo', 'melodía', 'melodia', 'tonalidad',
            'modalidad', 'tempo', 'compás', 'compas', 'escala', 'acorde',
            'disonancia', 'consonancia', 'modulación', 'modulacion', 'cadencia',
            'forma', 'estructura', 'desarrollo', 'exposición', 'exposicion',
            'recapitulación', 'recapitulacion', 'coda', 'tema', 'motivo',
            'frase', 'período', 'periodo', 'textura', 'contrapunto',
            'polifonía', 'polifonia', 'homofonía', 'homofonia', 'timbre',
            'dinámica', 'dinamica', 'articulación', 'articulacion'
        ]
        
        self.performance_terms = [
            'teatro', 'conservatorio', 'festival', 'concierto', 'recital',
            'interpretación', 'interpretacion', 'ejecución', 'ejecucion',
            'técnica', 'tecnica', 'estilo', 'expresión', 'expresion',
            'virtuosismo', 'maestría', 'maestria', 'director', 'directora',
            'intérprete', 'interprete', 'solista', 'concertista', 'virtuoso',
            'orquesta', 'banda', 'coro', 'ensemble', 'agrupación', 'agrupacion',
            'sala', 'auditorio', 'temporada', 'programa', 'repertorio'
        ]
        
        self.criticism_terms = [
            'crítica', 'critica', 'reseña', 'resena', 'análisis', 'analisis',
            'opinión', 'opinion', 'juicio', 'valoración', 'valoracion',
            'calidad', 'excelencia', 'mediocridad', 'defecto', 'virtud',
            'logro', 'éxito', 'exito', 'fracaso', 'triunfo', 'aplauso',
            'ovación', 'ovacion', 'silbido', 'protesta', 'admiración', 'admiracion'
        ]
        
        # All terms combined for comprehensive analysis
        self.all_musical_terms = (self.musical_genres + self.instruments + 
                                self.technical_terms + self.performance_terms + 
                                self.criticism_terms)
    
    def extract_date_from_filename(self, filename):
        """Extract date information from filename"""
        date_patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
            r'(\d{4})-(\d{1,2})',           # YYYY-MM
            r'(\d{4})',                     # YYYY only
            r'(\d{1,2})-(\d{4})',          # MM-YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, filename)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    return int(groups[0]), int(groups[1]), int(groups[2])
                elif len(groups) == 2:
                    if int(groups[0]) > 31:  # First number is year
                        return int(groups[0]), int(groups[1]), 1
                    else:  # First number is month
                        return int(groups[1]), int(groups[0]), 1
                else:
                    return int(groups[0]), 1, 1
        return None, None, None
    
    def extract_date_from_directory(self, directory_name):
        """Extract date range from directory name"""
        # Pattern for ranges like "1842-1845"
        range_pattern = r'(\d{4})-(\d{4})'
        match = re.search(range_pattern, directory_name)
        if match:
            return int(match.group(1)), int(match.group(2))
        
        # Pattern for single year
        single_pattern = r'(\d{4})'
        match = re.search(single_pattern, directory_name)
        if match:
            year = int(match.group(1))
            return year, year
        
        return None, None
    
    def count_words_in_file(self, filepath):
        """Count words in a text file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Simple word count (split by whitespace)
                words = len(content.split())
                return words, content.lower()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return 0, ""
    
    def analyze_musical_vocabulary(self, content):
        """Analyze musical vocabulary in content"""
        vocabulary_counts = {}
        
        # Count occurrences of each musical term
        for term in self.all_musical_terms:
            count = len(re.findall(r'\b' + re.escape(term) + r'\b', content, re.IGNORECASE))
            if count > 0:
                vocabulary_counts[term] = count
        
        return vocabulary_counts
    
    def analyze_magazine_directory(self, directory_path):
        """Analyze a single magazine directory"""
        magazine_name = os.path.basename(directory_path)
        print(f"Analyzing {magazine_name}...")
        
        # Extract date range from directory name
        start_year, end_year = self.extract_date_from_directory(magazine_name)
        
        magazine_data = {
            'name': magazine_name.replace('TXT-', '').replace('TXT ', '').replace('TXT-', '').strip(),
            'directory': directory_path,
            'start_year': start_year,
            'end_year': end_year,
            'files': [],
            'total_files': 0,
            'total_words': 0,
            'vocabulary_counts': Counter(),
            'years_active': set()
        }
        
        # Find all text files recursively
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.txt'):
                    filepath = os.path.join(root, file)
                    
                    # Extract date from filename
                    year, month, day = self.extract_date_from_filename(file)
                    
                    # Count words and analyze vocabulary
                    word_count, content = self.count_words_in_file(filepath)
                    vocabulary = self.analyze_musical_vocabulary(content)
                    
                    file_data = {
                        'filename': file,
                        'filepath': filepath,
                        'year': year,
                        'month': month,
                        'day': day,
                        'word_count': word_count,
                        'vocabulary': vocabulary
                    }
                    
                    magazine_data['files'].append(file_data)
                    magazine_data['total_words'] += word_count
                    
                    # Update vocabulary counts
                    for term, count in vocabulary.items():
                        magazine_data['vocabulary_counts'][term] += count
                    
                    # Track years active
                    if year:
                        magazine_data['years_active'].add(year)
        
        magazine_data['total_files'] = len(magazine_data['files'])
        magazine_data['years_active'] = sorted(list(magazine_data['years_active']))
        
        # Update actual date range based on files
        if magazine_data['years_active']:
            magazine_data['actual_start_year'] = min(magazine_data['years_active'])
            magazine_data['actual_end_year'] = max(magazine_data['years_active'])
        
        return magazine_data
    
    def categorize_by_historical_periods(self):
        """Categorize magazines by historical periods"""
        periods = {
            'Romántico Temprano (1842-1870)': [],
            'Romántico Tardío (1870-1900)': [],
            'Modernista (1900-1930)': [],
            'Vanguardia y Guerra Civil (1930-1960)': [],
            'Desarrollismo y Transición (1960-1990)': [],
            'Democracia y Era Digital (1990-2024)': []
        }
        
        for mag_name, mag_data in self.magazines_data.items():
            start_year = mag_data.get('actual_start_year') or mag_data.get('start_year')
            if not start_year:
                continue
                
            if start_year <= 1870:
                periods['Romántico Temprano (1842-1870)'].append(mag_name)
            elif start_year <= 1900:
                periods['Romántico Tardío (1870-1900)'].append(mag_name)
            elif start_year <= 1930:
                periods['Modernista (1900-1930)'].append(mag_name)
            elif start_year <= 1960:
                periods['Vanguardia y Guerra Civil (1930-1960)'].append(mag_name)
            elif start_year <= 1990:
                periods['Desarrollismo y Transición (1960-1990)'].append(mag_name)
            else:
                periods['Democracia y Era Digital (1990-2024)'].append(mag_name)
        
        return periods
    
    def get_top_terms_by_period(self, n=10):
        """Get top N musical terms by historical period"""
        periods_vocab = defaultdict(Counter)
        
        for mag_name, mag_data in self.magazines_data.items():
            start_year = mag_data.get('actual_start_year') or mag_data.get('start_year')
            if not start_year:
                continue
            
            # Determine period
            if start_year <= 1870:
                period = 'Romántico Temprano (1842-1870)'
            elif start_year <= 1900:
                period = 'Romántico Tardío (1870-1900)'
            elif start_year <= 1930:
                period = 'Modernista (1900-1930)'
            elif start_year <= 1960:
                period = 'Vanguardia y Guerra Civil (1930-1960)'
            elif start_year <= 1990:
                period = 'Desarrollismo y Transición (1960-1990)'
            else:
                period = 'Democracia y Era Digital (1990-2024)'
            
            # Add vocabulary counts to period
            for term, count in mag_data['vocabulary_counts'].items():
                periods_vocab[period][term] += count
        
        # Get top N terms for each period
        top_terms_by_period = {}
        for period, vocab_counter in periods_vocab.items():
            top_terms_by_period[period] = vocab_counter.most_common(n)
        
        return top_terms_by_period
    
    def analyze_genre_evolution(self):
        """Analyze evolution of musical genres over time"""
        genre_evolution = {}
        
        for genre in self.musical_genres:
            genre_evolution[genre] = {}
            
            for mag_name, mag_data in self.magazines_data.items():
                start_year = mag_data.get('actual_start_year') or mag_data.get('start_year')
                if start_year and genre in mag_data['vocabulary_counts']:
                    genre_evolution[genre][start_year] = mag_data['vocabulary_counts'][genre]
        
        return genre_evolution
    
    def run_comprehensive_analysis(self):
        """Run the complete analysis"""
        print("Starting comprehensive analysis of Spanish music magazines...")
        
        # Find all magazine directories
        magazine_dirs = []
        for item in os.listdir(self.base_directory):
            item_path = os.path.join(self.base_directory, item)
            if os.path.isdir(item_path) and ('TXT' in item or 'txt' in item):
                magazine_dirs.append(item_path)
        
        print(f"Found {len(magazine_dirs)} magazine directories")
        
        # Analyze each magazine
        for directory in sorted(magazine_dirs):
            magazine_data = self.analyze_magazine_directory(directory)
            self.magazines_data[magazine_data['name']] = magazine_data
            self.total_files += magazine_data['total_files']
            self.total_words += magazine_data['total_words']
        
        # Perform additional analyses
        historical_periods = self.categorize_by_historical_periods()
        top_terms_by_period = self.get_top_terms_by_period(10)
        genre_evolution = self.analyze_genre_evolution()
        
        # Calculate date range safely
        start_years = []
        end_years = []
        for mag in self.magazines_data.values():
            if mag.get('actual_start_year'):
                start_years.append(mag['actual_start_year'])
            elif mag.get('start_year'):
                start_years.append(mag['start_year'])
            
            if mag.get('actual_end_year'):
                end_years.append(mag['actual_end_year'])
            elif mag.get('end_year'):
                end_years.append(mag['end_year'])
        
        date_range = f"{min(start_years) if start_years else '?'}-{max(end_years) if end_years else '?'}"
        
        # Compile comprehensive results
        results = {
            'summary': {
                'total_magazines': len(self.magazines_data),
                'total_files': self.total_files,
                'total_words': self.total_words,
                'date_range': date_range
            },
            'magazines': self.magazines_data,
            'historical_periods': historical_periods,
            'top_terms_by_period': top_terms_by_period,
            'genre_evolution': genre_evolution,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def save_results(self, results, output_file='comprehensive_musical_magazines_analysis.json'):
        """Save results to JSON file"""
        # Convert Counter objects to regular dicts for JSON serialization
        def convert_counters(obj):
            if isinstance(obj, Counter):
                return dict(obj)
            elif isinstance(obj, dict):
                return {k: convert_counters(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_counters(item) for item in obj]
            elif isinstance(obj, set):
                return list(obj)
            else:
                return obj
        
        json_compatible_results = convert_counters(results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_compatible_results, f, ensure_ascii=False, indent=2)
        
        print(f"Results saved to {output_file}")
        return output_file

def main():
    base_directory = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS"
    
    analyzer = ComprehensiveMusicalMagazinesAnalyzer(base_directory)
    results = analyzer.run_comprehensive_analysis()
    
    # Save detailed results
    output_file = analyzer.save_results(results)
    
    # Print summary
    print("\n" + "="*80)
    print("COMPREHENSIVE SPANISH MUSIC MAGAZINES ANALYSIS SUMMARY")
    print("="*80)
    print(f"Total magazines analyzed: {results['summary']['total_magazines']}")
    print(f"Total files processed: {results['summary']['total_files']:,}")
    print(f"Total words counted: {results['summary']['total_words']:,}")
    print(f"Date range: {results['summary']['date_range']}")
    
    print("\nMAGAZINES BY CHRONOLOGICAL ORDER:")
    print("-"*50)
    
    # Sort magazines chronologically
    sorted_magazines = sorted(
        results['magazines'].items(),
        key=lambda x: x[1].get('actual_start_year') or x[1].get('start_year') or 9999
    )
    
    for i, (name, data) in enumerate(sorted_magazines, 1):
        start = data.get('actual_start_year') or data.get('start_year') or '?'
        end = data.get('actual_end_year') or data.get('end_year') or '?'
        print(f"{i:2d}. {name}")
        print(f"    Period: {start}-{end}")
        print(f"    Files: {data['total_files']:,} | Words: {data['total_words']:,}")
        print()
    
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == "__main__":
    main()