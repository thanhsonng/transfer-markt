import scrapy
import csv
import os

class TransferMarktSpider(scrapy.Spider):
    name = 'transfermarktspider'

    season = 2018
    matchday = 1
    start_urls = [f'https://www.transfermarkt.co.uk/laliga/spieltagtabelle/wettbewerb/ES1?saison_id={season}&spieltag={matchday}']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    }

    def parse(self, response):
        filename = f'./output/laliga/season_{self.season}/season_{self.season}_matchday_{self.matchday}.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as file:
            writer = csv.writer(file)

            headers = ['#', 'Club', 'Matches', 'W', 'D', 'L', 'Goals', '+/-', 'Pts']
            writer.writerow(headers)

            for row in response.css('table.items tbody tr'):
                data = []
                for index, field in enumerate(row.css('td')):
                    # Ignore club logo
                    if index == 1:
                        continue
                    # Get club name
                    if index == 2:
                        data.append(field.css('a::text').get().strip())
                        continue
                    data.append(field.css('::text').get().strip())
                writer.writerow(data)

            next_url = self.get_next_url()
            if next_url:
                yield response.follow(next_url, self.parse)


    def get_next_url(self):
        if self.matchday < 38:
            self.matchday += 1
        elif self.season < 2023:
            self.season += 1
            self.matchday = 1
        else:
            return None
        return f'https://www.transfermarkt.co.uk/laliga/spieltagtabelle/wettbewerb/ES1?saison_id={self.season}&spieltag={self.matchday}'
