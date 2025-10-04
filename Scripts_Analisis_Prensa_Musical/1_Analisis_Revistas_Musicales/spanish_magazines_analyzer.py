#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Analysis of Spanish Musical Magazines (1909-1926)
Analyzing 3,079 text files across multiple collections
"""

import os
import re
import json
from collections import defaultdict, Counter
from pathlib import Path
import unicodedata

class SpanishMagazineAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.results = {}
        
        # Define the 4 main magazines to analyze as requested
        self.target_magazines = {
            "ONDAS": "TXT - ONDAS año mes dia",
            "Revista Musical Hispanoamericana": "TXT - Revista Musical Hispanoamericana", 
            "Revista Musical de Bilbao": "TXT - Revista Musical de Bilbao",
            "Revista Triunfo": "TXT -RevistaTriunfo"
        }
        
        # Musical vocabulary and patterns
        self.musical_instruments = [
            # Strings
            'violín', 'viola', 'violonchelo', 'violoncello', 'contrabajo', 'arpa', 'guitarra', 'mandolina', 'laúd', 'bandurria',
            # Winds
            'flauta', 'oboe', 'clarinete', 'fagot', 'saxofón', 'trompa', 'trompeta', 'trombón', 'tuba', 'cornetín',
            # Percussion
            'timbal', 'timbales', 'tambor', 'bombo', 'platillos', 'triángulo', 'castañuelas', 'pandereta',
            # Keyboard
            'piano', 'órgano', 'harmonium', 'clavecín', 'clave', 'pianola',
            # Voice
            'soprano', 'contralto', 'tenor', 'bajo', 'barítono', 'mezzo-soprano'
        ]
        
        self.music_genres = [
            'ópera', 'opereta', 'zarzuela', 'sinfonía', 'concierto', 'sonata', 'cuarteto', 'quinteto',
            'vals', 'polka', 'mazurca', 'habanera', 'tango', 'pasodoble', 'jota', 'sardana', 'fandango',
            'misa', 'requiem', 'tedeum', 'salve', 'himno', 'marcha', 'fantasía', 'rapsodia', 'preludio',
            'fuga', 'canon', 'variaciones', 'suite', 'ballet', 'danza', 'minueto', 'gavota', 'sarabanda'
        ]
        
        self.venues = [
            'teatro', 'ópera', 'casino', 'ateneo', 'conservatorio', 'academia', 'salón', 'sala',
            'auditorio', 'coliseo', 'principal', 'liceo', 'real', 'nacional', 'municipal'
        ]
        
        # Common Spanish names for gender analysis
        self.male_names = [
            'josé', 'manuel', 'francisco', 'antonio', 'juan', 'miguel', 'luis', 'pedro', 'carlos', 'fernando',
            'rafael', 'vicente', 'eduardo', 'ricardo', 'alberto', 'pablo', 'ramón', 'gabriel', 'enrique', 'alfonso',
            'joaquín', 'mariano', 'emilio', 'andrés', 'tomás', 'guillermo', 'salvador', 'arturo', 'lorenzo', 'ignacio'
        ]
        
        self.female_names = [
            'maría', 'carmen', 'josefa', 'francisca', 'antonia', 'dolores', 'pilar', 'teresa', 'ana', 'isabel',
            'mercedes', 'rosario', 'ángeles', 'concepción', 'esperanza', 'asunción', 'cristina', 'elena', 'julia',
            'rosa', 'soledad', 'amparo', 'remedios', 'encarnación', 'catalina', 'manuela', 'emilia', 'consuelo'
        ]
        
        # Famous composers and musicians for frequency analysis
        self.composers = [
            # Spanish
            'albéniz', 'granados', 'falla', 'turina', 'bretón', 'chapí', 'barbieri', 'arrieta', 'pedrell', 'vives',
            'usandizaga', 'esplá', 'guridi', 'toldrà', 'rodrigo', 'halffter', 'nin', 'mompou', 'cassadó',
            # International 
            'bach', 'beethoven', 'mozart', 'wagner', 'verdi', 'puccini', 'rossini', 'chopin', 'liszt', 'brahms',
            'schumann', 'mendelssohn', 'schubert', 'haydn', 'handel', 'vivaldi', 'tchaikovsky', 'rimsky-korsakov',
            'debussy', 'ravel', 'bizet', 'massenet', 'saint-saëns', 'franck', 'strauss', 'mahler'
        ]

    def normalize_text(self, text):
        """Normalize Spanish text for analysis"""
        # Convert to lowercase
        text = text.lower()
        # Remove accents but keep ñ
        text = ''.join(c for c in unicodedata.normalize('NFD', text) 
                      if unicodedata.category(c) != 'Mn' or c in 'ñ')
        return text

    def extract_dates_from_filename(self, filename):
        """Extract publication dates from filenames"""
        # Pattern for ONDAS: O-1925-10-11.txt
        ondas_match = re.search(r'O-(\d{4})-(\d{1,2})-(\d{1,2})\.txt', filename)
        if ondas_match:
            return int(ondas_match.group(1)), int(ondas_match.group(2))
            
        # Pattern for musical magazines: 1914-1-Revista...
        mag_match = re.search(r'(\d{4})-(\d{1,2})-', filename)
        if mag_match:
            return int(mag_match.group(1)), int(mag_match.group(2))
            
        # Pattern for Triunfo: RTXIX~N101~P54-55 (more complex)
        triunfo_match = re.search(r'RT([XVI]+)', filename)
        if triunfo_match:
            # Convert Roman numerals to approximate years (this would need more precise mapping)
            roman = triunfo_match.group(1)
            # This is a simplified mapping - real implementation would need precise year mapping
            return None, None
            
        return None, None

    def count_musical_elements(self, text):
        """Count occurrences of musical elements in text"""
        normalized_text = self.normalize_text(text)
        
        counts = {
            'instruments': Counter(),
            'genres': Counter(), 
            'venues': Counter(),
            'composers': Counter()
        }
        
        # Count instruments
        for instrument in self.musical_instruments:
            pattern = r'\b' + re.escape(instrument) + r'\w*\b'
            matches = len(re.findall(pattern, normalized_text))
            if matches > 0:
                counts['instruments'][instrument] = matches
                
        # Count genres
        for genre in self.music_genres:
            pattern = r'\b' + re.escape(genre) + r'\w*\b'
            matches = len(re.findall(pattern, normalized_text))
            if matches > 0:
                counts['genres'][genre] = matches
                
        # Count venues
        for venue in self.venues:
            pattern = r'\b' + re.escape(venue) + r'\w*\b'
            matches = len(re.findall(pattern, normalized_text))
            if matches > 0:
                counts['venues'][venue] = matches
                
        # Count composers
        for composer in self.composers:
            pattern = r'\b' + re.escape(composer) + r'\w*\b'
            matches = len(re.findall(pattern, normalized_text))
            if matches > 0:
                counts['composers'][composer] = matches
                
        return counts

    def analyze_gender(self, text):
        """Analyze gender representation in personal names"""
        normalized_text = self.normalize_text(text)
        
        male_count = 0
        female_count = 0
        
        for name in self.male_names:
            pattern = r'\b' + re.escape(name) + r'\b'
            male_count += len(re.findall(pattern, normalized_text))
            
        for name in self.female_names:
            pattern = r'\b' + re.escape(name) + r'\b'
            female_count += len(re.findall(pattern, normalized_text))
            
        return male_count, female_count

    def analyze_spanish_vs_foreign(self, text):
        """Analyze Spanish vs foreign musical content"""
        normalized_text = self.normalize_text(text)
        
        spanish_composers = ['albéniz', 'granados', 'falla', 'turina', 'bretón', 'chapí', 'barbieri', 
                           'arrieta', 'pedrell', 'vives', 'usandizaga', 'esplá', 'guridi', 'toldrà']
        foreign_composers = ['bach', 'beethoven', 'mozart', 'wagner', 'verdi', 'puccini', 'rossini', 
                           'chopin', 'liszt', 'brahms', 'schumann', 'mendelssohn', 'schubert']
        
        spanish_mentions = 0
        foreign_mentions = 0
        
        for composer in spanish_composers:
            spanish_mentions += len(re.findall(r'\b' + re.escape(composer) + r'\w*\b', normalized_text))
            
        for composer in foreign_composers:
            foreign_mentions += len(re.findall(r'\b' + re.escape(composer) + r'\w*\b', normalized_text))
            
        return spanish_mentions, foreign_mentions

    def analyze_magazine(self, magazine_name, directory_name):
        """Analyze a single magazine collection"""
        print(f"Analyzing {magazine_name}...")
        
        magazine_path = self.base_path / directory_name
        if not magazine_path.exists():
            print(f"Directory not found: {magazine_path}")
            return None
            
        results = {
            'name': magazine_name,
            'directory': directory_name,
            'files_processed': 0,
            'total_words': 0,
            'instruments': Counter(),
            'genres': Counter(),
            'venues': Counter(),
            'composers': Counter(),
            'male_names': 0,
            'female_names': 0,
            'spanish_composers': 0,
            'foreign_composers': 0,
            'years_covered': set(),
            'file_details': []
        }
        
        # Find all text files (both .txt and files without extension for Triunfo)
        if magazine_name == "Revista Triunfo":
            files = [f for f in magazine_path.iterdir() if f.is_file() and not f.name.startswith('.')]
        else:
            files = list(magazine_path.glob("*.txt"))
            
        files.sort()
        
        for file_path in files:
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                if not content.strip():  # Skip empty files
                    continue
                    
                results['files_processed'] += 1
                word_count = len(content.split())
                results['total_words'] += word_count
                
                # Extract dates
                year, month = self.extract_dates_from_filename(file_path.name)
                if year:
                    results['years_covered'].add(year)
                
                # Count musical elements
                musical_counts = self.count_musical_elements(content)
                for category, counter in musical_counts.items():
                    results[category].update(counter)
                
                # Gender analysis
                male, female = self.analyze_gender(content)
                results['male_names'] += male
                results['female_names'] += female
                
                # Spanish vs foreign analysis
                spanish, foreign = self.analyze_spanish_vs_foreign(content)
                results['spanish_composers'] += spanish
                results['foreign_composers'] += foreign
                
                # Store file details
                results['file_details'].append({
                    'filename': file_path.name,
                    'words': word_count,
                    'year': year,
                    'month': month
                })
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Convert years set to sorted list
        results['years_covered'] = sorted(list(results['years_covered']))
        
        print(f"Completed {magazine_name}: {results['files_processed']} files, {results['total_words']:,} words")
        return results

    def run_analysis(self):
        """Run complete analysis of all requested magazines"""
        print("Starting comprehensive analysis of Spanish musical magazines...")
        
        for magazine_name, directory_name in self.target_magazines.items():
            result = self.analyze_magazine(magazine_name, directory_name)
            if result:
                self.results[magazine_name] = result
        
        return self.results

    def generate_report(self):
        """Generate comprehensive analytical report"""
        if not self.results:
            return "No analysis results available."
            
        report = []
        report.append("="*80)
        report.append("COMPREHENSIVE ANALYSIS OF SPANISH MUSICAL MAGAZINES (1909-1926)")
        report.append("="*80)
        report.append("")
        
        # Summary statistics
        total_files = sum(r['files_processed'] for r in self.results.values())
        total_words = sum(r['total_words'] for r in self.results.values())
        
        report.append(f"TOTAL FILES ANALYZED: {total_files}")
        report.append(f"TOTAL WORDS PROCESSED: {total_words:,}")
        report.append("")
        
        # Individual magazine analysis
        for magazine_name, data in self.results.items():
            report.append("="*60)
            report.append(f"MAGAZINE: {magazine_name}")
            report.append("="*60)
            report.append(f"Period covered: {min(data['years_covered']) if data['years_covered'] else 'Unknown'}-{max(data['years_covered']) if data['years_covered'] else 'Unknown'}")
            report.append(f"Files processed: {data['files_processed']}")
            report.append(f"Total words: {data['total_words']:,}")
            report.append("")
            
            # Top composers
            if data['composers']:
                report.append("TOP 20 MOST MENTIONED MUSICIANS/COMPOSERS:")
                for composer, count in data['composers'].most_common(20):
                    report.append(f"  {composer.capitalize()}: {count} mentions")
                report.append("")
            
            # Top instruments
            if data['instruments']:
                report.append("TOP 15 MUSICAL INSTRUMENTS:")
                for instrument, count in data['instruments'].most_common(15):
                    report.append(f"  {instrument.capitalize()}: {count} mentions")
                report.append("")
            
            # Genre distribution
            if data['genres']:
                total_genre_mentions = sum(data['genres'].values())
                report.append("MUSIC GENRE DISTRIBUTION:")
                for genre, count in data['genres'].most_common(10):
                    percentage = (count / total_genre_mentions) * 100
                    report.append(f"  {genre.capitalize()}: {count} ({percentage:.1f}%)")
                report.append("")
            
            # Gender analysis
            total_names = data['male_names'] + data['female_names']
            if total_names > 0:
                male_pct = (data['male_names'] / total_names) * 100
                female_pct = (data['female_names'] / total_names) * 100
                report.append("GENDER REPRESENTATION:")
                report.append(f"  Male names: {data['male_names']} ({male_pct:.1f}%)")
                report.append(f"  Female names: {data['female_names']} ({female_pct:.1f}%)")
                report.append("")
            
            # Spanish vs Foreign
            total_composer_mentions = data['spanish_composers'] + data['foreign_composers']
            if total_composer_mentions > 0:
                spanish_pct = (data['spanish_composers'] / total_composer_mentions) * 100
                foreign_pct = (data['foreign_composers'] / total_composer_mentions) * 100
                report.append("SPANISH VS FOREIGN MUSICAL WORKS:")
                report.append(f"  Spanish composers: {data['spanish_composers']} ({spanish_pct:.1f}%)")
                report.append(f"  Foreign composers: {data['foreign_composers']} ({foreign_pct:.1f}%)")
                report.append("")
            
            # Venues
            if data['venues']:
                report.append("CONCERT VENUES/TYPES:")
                for venue, count in data['venues'].most_common(10):
                    report.append(f"  {venue.capitalize()}: {count} mentions")
                report.append("")
        
        # Comparative analysis
        report.append("="*60)
        report.append("COMPARATIVE ANALYSIS")
        report.append("="*60)
        
        # Chronological evolution
        report.append("CHRONOLOGICAL COVERAGE:")
        for magazine_name, data in self.results.items():
            if data['years_covered']:
                report.append(f"  {magazine_name}: {min(data['years_covered'])}-{max(data['years_covered'])}")
        report.append("")
        
        # Size comparison
        report.append("MAGAZINE SIZE COMPARISON (by word count):")
        sorted_magazines = sorted(self.results.items(), key=lambda x: x[1]['total_words'], reverse=True)
        for magazine_name, data in sorted_magazines:
            report.append(f"  {magazine_name}: {data['total_words']:,} words")
        report.append("")
        
        return "\n".join(report)

def main():
    base_path = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS"
    analyzer = SpanishMagazineAnalyzer(base_path)
    
    # Run analysis
    results = analyzer.run_analysis()
    
    # Generate and save report
    report = analyzer.generate_report()
    
    # Save results to file
    with open("/Users/maria/spanish_magazines_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Save raw data as JSON
    # Convert Counter objects to dictionaries for JSON serialization
    json_results = {}
    for mag_name, data in results.items():
        json_data = dict(data)
        for key in ['instruments', 'genres', 'venues', 'composers']:
            json_data[key] = dict(json_data[key])
        json_results[mag_name] = json_data
    
    with open("/Users/maria/spanish_magazines_raw_data.json", "w", encoding="utf-8") as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    
    print("Analysis complete! Check the generated report files.")
    return report

if __name__ == "__main__":
    main()