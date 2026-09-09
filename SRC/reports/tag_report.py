import pandas as pd
import json
from collections import Counter
from datetime import datetime

class TagReporter:
    def __init__(self, skill_df, unique_df):
        self.skill_data = skill_df
        self.unique_data = unique_df
    
    def generate_tag_analysis(self):
        """Etiket analizi raporu oluşturur"""
        report = {
            'date': datetime.now().isoformat(),
            'skill_analysis': {},
            'unique_analysis': {},
            'summary': {}
        }
        
        # Skill etiket analizi
        if self.skill_data is not None:
            all_tags = []
            for tags in self.skill_data['parsed_tags']:
                if pd.notna(tags):
                    all_tags.extend(str(tags).split('|'))
            
            tag_counts = Counter(all_tags)
            report['skill_analysis'] = {
                'total_skills': len(self.skill_data),
                'tag_counts': dict(tag_counts.most_common(10)),
                'damage_distribution': self.skill_data['damage_type'].value_counts().to_dict(),
                'skill_type_distribution': self.skill_data['skill_type'].value_counts().to_dict()
            }
        
        # Unique etiket analizi
        if self.unique_data is not None:
            slot_counts = self.unique_data['slot'].value_counts().to_dict()
            report['unique_analysis'] = {
                'total_uniques': len(self.unique_data),
                'slot_distribution': slot_counts,
                'stat_tags': {}
            }
        
        # Özet
        report['summary'] = {
            'total_items': len(self.skill_data) + len(self.unique_data) if self.skill_data is not None and self.unique_data is not None else 0,
            'total_skill_tags': len(report['skill_analysis'].get('tag_counts', {})),
            'top_tags': list(report['skill_analysis'].get('tag_counts', {}).keys())[:5]
        }
        
        return report

# Kullanım
if __name__ == "__main__":
    # Verileri yükle
    skill_df = pd.read_csv('DATA/processed/skills_with_tags.csv')
    unique_df = pd.read_csv('DATA/processed/uniques_with_tags.csv')
    
    reporter = TagReporter(skill_df, unique_df)
    report = reporter.generate_tag_analysis()
    
    # Raporu kaydet
    import os
    os.makedirs('OUTPUTS/reports/daily', exist_ok=True)
    with open('OUTPUTS/reports/daily/tag_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📊 Tag analizi tamamlandı!")
    print(f"Toplam tag: {report['summary']['total_skill_tags']}")
    print(f"En popüler tag'ler: {', '.join(report['summary']['top_tags'])}")
