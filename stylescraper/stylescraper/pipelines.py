# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StylescraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        # Strip whitespace from strings and switch to lowercase
        field_names = ["name", "descriptions", "rel_aesthetics", "key_colors", "brands"] #adapter.field_names()
        print("***********************************")
        print(field_names)
        for field_name in field_names:
            value = adapter.get(field_name)
            if not value:
                continue
            # If value is tuple (always size 1), extract
            if type(value) == tuple:
                    value = value[0]

            if type(value) == str:
                adapter[field_name] = value.strip().lower()
                continue

            # If value is a list, iterate through
            else:            
                new_values = []
                for i in range(len(value)):
                    try:
                        new_val = value.strip().lower()
                    except:
                        new_val = value[i].strip().lower()
                    # Remove empty strings and singular symbols
                    if (len(new_val) > 1): 
                        new_values.append(new_val)
                adapter[field_name] = new_values
        
        
        return item
    
