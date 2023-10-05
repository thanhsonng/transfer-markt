import scrapy
import csv

class TransferMarktSpider(scrapy.Spider):
    name = 'transfermarktspider'

    season = 2022
    matchday = 1
    start_urls = [f'https://www.transfermarkt.co.uk/premier-league/spieltagtabelle/wettbewerb/GB1?saison_id=2022&spieltag=1']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    }

    def parse(self, response):
        with open(f'./output/season_{self.season}_matchday_{self.matchday}.csv', 'w') as file:
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

            if self.matchday < 38:
                self.matchday += 1
                yield response.follow(self.get_url(), self.parse)


    def get_url(self):
        return f'https://www.transfermarkt.co.uk/premier-league/spieltagtabelle/wettbewerb/GB1?saison_id={self.season}&spieltag={self.matchday}'
