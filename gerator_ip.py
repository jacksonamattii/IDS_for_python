
import requests
from bs4 import BeautifulSoup

URL = "https://www.projecthoneypot.org/list_of_ips.php" 
response = requests.get(URL)  # Obtém a resposta HTTP

soup = BeautifulSoup(response.text, 'html.parser')  

ip_addresses = [] 
for row in soup.select('table.manmx tr')[1:]:  # Seleciona as linhas da tabela ignorando o cabeçalho
    ip_cell = row.select_one('td a.bnone')  
    if ip_cell:
        ip_addresses.append(ip_cell.text.strip())  

# Salvar os IPs no arquivo
with open('iplist.txt', 'w') as file:  
    for ip in ip_addresses:  
        print(ip)  
        file.write(ip + '\n')  

