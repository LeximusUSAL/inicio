#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Analysis of Boletín Musical (1893-1918)
Statistical Analysis for Web Publishing
"""

import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import unicodedata

class BoletinMusicalAnalyzer:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.results = {
            'total_files': 0,
            'total_words': 0,
            'word_count_by_year': {},
            'issues_by_year': {},
            'musical_vocabulary': {
                'instruments': Counter(),
                'musical_forms': Counter(),
                'technical_terms': Counter(),
                'musical_terminology': Counter(),
                'positions_roles': Counter()
            },
            'notable_names': {
                'composers': Counter(),
                'musicians': Counter(),
                'institutions': Counter(),
                'theaters': Counter(),
                'other_personalities': Counter()
            },
            'themes_topics': {
                'reviews_critiques': 0,
                'educational_content': 0,
                'news_announcements': 0,
                'theory_articles': 0,
                'composer_profiles': 0,
                'advertisements': 0,
                'editorials': 0
            },
            'temporal_analysis': {},
            'file_details': []
        }
        
        # Define musical vocabulary dictionaries
        self.init_musical_vocabularies()
        
    def init_musical_vocabularies(self):
        """Initialize comprehensive musical vocabulary lists"""
        
        # Musical instruments (in Spanish)
        self.instruments = {
            'piano', 'violín', 'guitarra', 'gaita', 'órgano', 'arpa', 'flauta',
            'clarinete', 'oboe', 'fagot', 'trompeta', 'trompa', 'trombón',
            'violoncello', 'viola', 'contrabajo', 'corneta', 'bombardino',
            'tuba', 'tambor', 'timbales', 'castañuelas', 'bandurria', 'laúd',
            'dulzaina', 'cornamusa', 'zanfoña', 'sinfonia', 'harmonium',
            'acordeón', 'mandolina', 'cítara', 'lira', 'archilaúd', 'vihuela',
            'clave', 'clavicordio', 'rabel', 'chirimía', 'sacabuche', 'bajón'
        }
        
        # Musical forms and structures
        self.musical_forms = {
            'fuga', 'canon', 'contrapunto', 'sinfonía', 'concierto', 'sonata',
            'ópera', 'zarzuela', 'misa', 'motete', 'madrigal', 'villancico',
            'romance', 'copla', 'seguidilla', 'fandango', 'bolero', 'jota',
            'muiñeira', 'sardana', 'pasodoble', 'vals', 'mazurka', 'polonesa',
            'marcha', 'himno', 'serenata', 'nocturno', 'impromptu', 'estudio',
            'preludio', 'fantasía', 'variaciones', 'rondó', 'scherzo', 'minueto',
            'gavota', 'sarabanda', 'giga', 'allemanda', 'courante', 'chacona',
            'passacaglia', 'toccata', 'ricercare', 'capricho', 'bagatela'
        }
        
        # Technical musical terms
        self.technical_terms = {
            'armonía', 'melodía', 'ritmo', 'tonalidad', 'modulación', 'cadencia',
            'acorde', 'intervalo', 'escala', 'modo', 'compás', 'tiempo', 'movimiento',
            'tempo', 'agógica', 'dinámica', 'articulación', 'fraseo', 'expresión',
            'ornamentación', 'improvisación', 'transposición', 'enharmonía',
            'cromatismo', 'diatonismo', 'polifonía', 'homofonía', 'textura',
            'timbre', 'registro', 'tessitura', 'afinación', 'temperamento',
            'resolución', 'progresión', 'secuencia', 'imitación', 'desarrollo',
            'exposición', 'reexposición', 'coda', 'puente', 'episodio', 'stretto'
        }
        
        # Musical terminology and directions
        self.musical_terminology = {
            'allegro', 'andante', 'adagio', 'largo', 'presto', 'moderato',
            'andantino', 'allegretto', 'vivace', 'con brio', 'espressivo',
            'dolce', 'cantabile', 'maestoso', 'grazioso', 'scherzando',
            'staccato', 'legato', 'portato', 'tenuto', 'sforzando', 'crescendo',
            'diminuendo', 'forte', 'piano', 'fortissimo', 'pianissimo',
            'mezzo-forte', 'mezzo-piano', 'accelerando', 'ritardando',
            'rallentando', 'rubato', 'fermata', 'da capo', 'dal segno',
            'fine', 'coda', 'segue', 'attacca', 'tacet', 'pizzicato', 'arco',
            'con sordina', 'senza sordina', 'tremolo', 'vibrato', 'glissando'
        }
        
        # Musical positions and roles
        self.positions_roles = {
            'director', 'concertador', 'maestro', 'músico mayor', 'organista',
            'pianista', 'violinista', 'guitarrista', 'flautista', 'clarinetista',
            'trompetista', 'compositor', 'solista', 'concertista', 'virtuoso',
            'intérprete', 'ejecutante', 'cantante', 'tenor', 'soprano',
            'contralto', 'barítono', 'bajo', 'coro', 'orquesta', 'banda',
            'capilla', 'agrupación', 'ensemble', 'cuarteto', 'quinteto',
            'sexteto', 'orfeón', 'coral', 'capellán', 'beneficiado', 'chantre'
        }
        
        # Notable composers and musicians (common in Spanish music history)
        self.known_composers = {
            'barbieri', 'bretón', 'chapí', 'arrieta', 'eslava', 'pedrell',
            'albéniz', 'granados', 'turina', 'falla', 'vives', 'serrano',
            'caballero', 'chueca', 'valverde', 'fernández caballero',
            'marqués', 'oudrid', 'gaztambide', 'hernando', 'inzenga',
            'giner', 'goula', 'wagner', 'verdi', 'puccini', 'bizet',
            'mozart', 'beethoven', 'bach', 'chopin', 'liszt', 'brahms',
            'schumann', 'mendelssohn', 'schubert', 'haydn', 'handel',
            'rossini', 'donizetti', 'bellini', 'gounod', 'massenet',
            'saint-saëns', 'debussy', 'ravel', 'berlioz', 'franck',
            'varela silvari', 'sbarbi', 'arroyo', 'redondo', 'estruch',
            'enríquez', 'salinas', 'abascal', 'lacal', 'calvo', 'burgét',
            'francés', 'garcí­a rubio', 'benedito', 'wagener'
        }
        
        # Theaters and institutions
        self.known_institutions = {
            'conservatorio', 'escuela nacional de música', 'real conservatorio',
            'ateneo', 'sociedad de conciertos', 'teatro real', 'teatro de la ópera',
            'teatro apolo', 'teatro de la zarzuela', 'teatro martín', 'teatro benavente',
            'catedral', 'iglesia', 'capilla real', 'banda municipal', 'orquesta sinfónica',
            'sociedad de autores', 'círculo de bellas artes', 'liceo', 'filarmónica'
        }

    def clean_text(self, text):
        """Clean and normalize text for analysis"""
        # Remove line numbers and formatting artifacts
        text = re.sub(r'^\s*\d+→', '', text, flags=re.MULTILINE)
        # Remove special characters but keep Spanish accents
        text = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ]', ' ', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()

    def extract_date_from_filename(self, filename):
        """Extract date information from filename"""
        # Pattern: Boletin-musical-Madrid-DD-MM-YYYY.txt
        pattern = r'Boletin-musical-Madrid-(\d{1,2})-(\d{1,2})-(\d{4})'
        match = re.search(pattern, filename)
        if match:
            day, month, year = match.groups()
            return {
                'day': int(day),
                'month': int(month), 
                'year': int(year),
                'date_string': f"{day}-{month}-{year}"
            }
        return None

    def count_words(self, text):
        """Count words in text"""
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()
        return len(words)

    def analyze_musical_vocabulary(self, text):
        """Analyze musical vocabulary in text"""
        cleaned_text = self.clean_text(text)
        words = set(cleaned_text.split())
        
        results = {
            'instruments': [],
            'musical_forms': [],
            'technical_terms': [],
            'musical_terminology': [],
            'positions_roles': []
        }
        
        # Check for instruments
        for word in words:
            if word in self.instruments:
                results['instruments'].append(word)
                self.results['musical_vocabulary']['instruments'][word] += 1
                
        # Check for musical forms
        for word in words:
            if word in self.musical_forms:
                results['musical_forms'].append(word)
                self.results['musical_vocabulary']['musical_forms'][word] += 1
                
        # Check for technical terms
        for word in words:
            if word in self.technical_terms:
                results['technical_terms'].append(word)
                self.results['musical_vocabulary']['technical_terms'][word] += 1
                
        # Check for musical terminology
        for word in words:
            if word in self.musical_terminology:
                results['musical_terminology'].append(word)
                self.results['musical_vocabulary']['musical_terminology'][word] += 1
                
        # Check for positions/roles
        for word in words:
            if word in self.positions_roles:
                results['positions_roles'].append(word)
                self.results['musical_vocabulary']['positions_roles'][word] += 1
                
        return results

    def extract_notable_names(self, text):
        """Extract notable names from text"""
        cleaned_text = self.clean_text(text)
        
        # Check for known composers
        for composer in self.known_composers:
            if composer in cleaned_text:
                self.results['notable_names']['composers'][composer] += 1
                
        # Check for institutions
        for institution in self.known_institutions:
            if institution in cleaned_text:
                self.results['notable_names']['institutions'][institution] += 1

    def classify_content(self, text, filename):
        """Classify content type"""
        cleaned_text = self.clean_text(text)
        
        # Keywords for different content types
        review_keywords = ['crítica', 'reseña', 'juicio', 'opinión', 'estreno', 'representación']
        educational_keywords = ['enseñanza', 'método', 'estudio', 'ejercicio', 'lección', 'teoría']
        news_keywords = ['noticia', 'anuncio', 'información', 'comunica', 'participa']
        theory_keywords = ['armonía', 'contrapunto', 'composición', 'técnica', 'forma']
        composer_keywords = ['biografía', 'maestro', 'compositor', 'vida', 'obra']
        ad_keywords = ['anuncio', 'venta', 'precio', 'almacén', 'casa editorial']
        editorial_keywords = ['editorial', 'redacción', 'propósito', 'programa', 'misión']
        
        # Score each content type
        scores = {
            'reviews_critiques': sum(1 for kw in review_keywords if kw in cleaned_text),
            'educational_content': sum(1 for kw in educational_keywords if kw in cleaned_text),
            'news_announcements': sum(1 for kw in news_keywords if kw in cleaned_text),
            'theory_articles': sum(1 for kw in theory_keywords if kw in cleaned_text),
            'composer_profiles': sum(1 for kw in composer_keywords if kw in cleaned_text),
            'advertisements': sum(1 for kw in ad_keywords if kw in cleaned_text),
            'editorials': sum(1 for kw in editorial_keywords if kw in cleaned_text)
        }
        
        # Classify based on highest score
        if max(scores.values()) > 0:
            content_type = max(scores, key=scores.get)
            self.results['themes_topics'][content_type] += 1
            return content_type
        
        return 'unclassified'

    def analyze_file(self, filepath):
        """Analyze a single file"""
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return None
            
        # Extract date information
        date_info = self.extract_date_from_filename(filename)
        
        # Count words
        word_count = self.count_words(content)
        
        # Analyze musical vocabulary
        musical_vocab = self.analyze_musical_vocabulary(content)
        
        # Extract notable names
        self.extract_notable_names(content)
        
        # Classify content
        content_type = self.classify_content(content, filename)
        
        # Update results
        if date_info:
            year = date_info['year']
            if year not in self.results['word_count_by_year']:
                self.results['word_count_by_year'][year] = 0
                self.results['issues_by_year'][year] = 0
            
            self.results['word_count_by_year'][year] += word_count
            self.results['issues_by_year'][year] += 1
            
            if year not in self.results['temporal_analysis']:
                self.results['temporal_analysis'][year] = {
                    'issues': [],
                    'total_words': 0,
                    'musical_terms_count': 0
                }
            
            musical_terms_count = sum(len(terms) for terms in musical_vocab.values())
            self.results['temporal_analysis'][year]['issues'].append({
                'filename': filename,
                'date': date_info['date_string'],
                'word_count': word_count,
                'content_type': content_type,
                'musical_terms': musical_terms_count
            })
            self.results['temporal_analysis'][year]['total_words'] += word_count
            self.results['temporal_analysis'][year]['musical_terms_count'] += musical_terms_count
        
        file_details = {
            'filename': filename,
            'word_count': word_count,
            'date_info': date_info,
            'content_type': content_type,
            'musical_vocabulary': musical_vocab
        }
        
        self.results['file_details'].append(file_details)
        self.results['total_words'] += word_count
        
        return file_details

    def analyze_all_files(self):
        """Analyze all files in the directory"""
        txt_files = [f for f in os.listdir(self.directory_path) if f.endswith('.txt')]
        self.results['total_files'] = len(txt_files)
        
        print(f"Analyzing {len(txt_files)} files...")
        
        for i, filename in enumerate(txt_files, 1):
            filepath = os.path.join(self.directory_path, filename)
            print(f"Processing {i}/{len(txt_files)}: {filename}")
            self.analyze_file(filepath)
        
        print("Analysis complete!")

    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = f"""
# ANÁLISIS ESTADÍSTICO COMPREHENSIVO
## BOLETÍN MUSICAL (1893-1918)

## 1. RESUMEN GENERAL
- **Total de archivos analizados**: {self.results['total_files']}
- **Total de palabras**: {self.results['total_words']:,}
- **Periodo temporal**: {min(self.results['issues_by_year'].keys()) if self.results['issues_by_year'] else 'N/A'} - {max(self.results['issues_by_year'].keys()) if self.results['issues_by_year'] else 'N/A'}

## 2. ANÁLISIS TEMPORAL

### Distribución por año:
"""
        
        for year in sorted(self.results['issues_by_year'].keys()):
            issues = self.results['issues_by_year'][year]
            words = self.results['word_count_by_year'][year]
            report += f"- **{year}**: {issues} números, {words:,} palabras\n"
        
        report += f"\n## 3. LÉXICO MUSICAL\n\n"
        
        # Musical instruments
        report += "### Instrumentos musicales más mencionados:\n"
        for instrument, count in self.results['musical_vocabulary']['instruments'].most_common(20):
            report += f"- {instrument}: {count} menciones\n"
        
        # Musical forms
        report += "\n### Formas musicales más mencionadas:\n"
        for form, count in self.results['musical_vocabulary']['musical_forms'].most_common(20):
            report += f"- {form}: {count} menciones\n"
        
        # Technical terms
        report += "\n### Términos técnicos más utilizados:\n"
        for term, count in self.results['musical_vocabulary']['technical_terms'].most_common(20):
            report += f"- {term}: {count} menciones\n"
        
        # Musical terminology
        report += "\n### Terminología musical más frecuente:\n"
        for term, count in self.results['musical_vocabulary']['musical_terminology'].most_common(20):
            report += f"- {term}: {count} menciones\n"
        
        # Positions and roles
        report += "\n### Posiciones y roles musicales:\n"
        for role, count in self.results['musical_vocabulary']['positions_roles'].most_common(20):
            report += f"- {role}: {count} menciones\n"
        
        # Notable names
        report += "\n## 4. PERSONALIDADES DESTACADAS\n\n"
        
        report += "### Compositores más mencionados:\n"
        for composer, count in self.results['notable_names']['composers'].most_common(20):
            report += f"- {composer}: {count} menciones\n"
        
        report += "\n### Instituciones más mencionadas:\n"
        for institution, count in self.results['notable_names']['institutions'].most_common(15):
            report += f"- {institution}: {count} menciones\n"
        
        # Content themes
        report += "\n## 5. TEMAS Y CONTENIDOS\n\n"
        
        total_classified = sum(self.results['themes_topics'].values())
        for theme, count in self.results['themes_topics'].items():
            if count > 0:
                percentage = (count / total_classified * 100) if total_classified > 0 else 0
                theme_name = theme.replace('_', ' ').title()
                report += f"- **{theme_name}**: {count} artículos ({percentage:.1f}%)\n"
        
        # Temporal evolution
        report += "\n## 6. EVOLUCIÓN TEMPORAL\n\n"
        
        for year in sorted(self.results['temporal_analysis'].keys()):
            year_data = self.results['temporal_analysis'][year]
            avg_words = year_data['total_words'] / len(year_data['issues']) if year_data['issues'] else 0
            avg_musical_terms = year_data['musical_terms_count'] / len(year_data['issues']) if year_data['issues'] else 0
            
            report += f"### {year}:\n"
            report += f"- Números publicados: {len(year_data['issues'])}\n"
            report += f"- Palabras promedio por número: {avg_words:.0f}\n"
            report += f"- Términos musicales promedio por número: {avg_musical_terms:.1f}\n"
            report += f"- Fechas de publicación: {', '.join([issue['date'] for issue in year_data['issues'][:5]])}\n"
            if len(year_data['issues']) > 5:
                report += f"  ... y {len(year_data['issues']) - 5} más\n"
            report += "\n"
        
        return report

    def save_results(self, output_dir="/Users/maria"):
        """Save results to files"""
        # Save JSON data
        json_path = os.path.join(output_dir, "boletin_musical_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            # Convert Counter objects to regular dicts for JSON serialization
            json_data = {}
            for key, value in self.results.items():
                if isinstance(value, dict):
                    json_data[key] = {}
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, Counter):
                            json_data[key][subkey] = dict(subvalue)
                        else:
                            json_data[key][subkey] = subvalue
                else:
                    json_data[key] = value
            
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        # Save comprehensive report
        report_path = os.path.join(output_dir, "boletin_musical_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        
        print(f"Results saved to:")
        print(f"- JSON data: {json_path}")
        print(f"- Report: {report_path}")

def main():
    directory_path = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS/TXT-Boletín Musical 1893-1918"
    
    analyzer = BoletinMusicalAnalyzer(directory_path)
    analyzer.analyze_all_files()
    
    # Generate and print report
    report = analyzer.generate_report()
    print("\n" + "="*80)
    print("COMPREHENSIVE ANALYSIS REPORT")
    print("="*80)
    print(report)
    
    # Save results
    analyzer.save_results()

if __name__ == "__main__":
    main()