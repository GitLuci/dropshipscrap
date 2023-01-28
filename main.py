import time
import os
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
from selenium.common.exceptions import NoSuchElementException

produto= ""
indiceproduto= 0
sites = ["https://pt.aliexpress.com/?gatewayAdapt=glo2bra","https://www.amazon.com"]
local_envio = "Brazil"

def configNav():
    #define o navegador
    option = webdriver.ChromeOptions()
    #option.add_argument('--headless') #deixa o navegador em segundo plano
    nav = webdriver.Chrome(options=option) #atribui ao navegador as opções
    return nav

def abrirNavegador(site,fazer):
    navegador = configNav()
    # passa ao navegador o site que deve abrir
    navegador.get(site)
    # tempo para o site ser carregado
    if fazer == "busca":
        if "aliexpress" in site:
            buscarAliexpress(navegador)
    elif fazer == "down":
        if "aliexpress" in site:
            baixarAliexpress(navegador)

def baixarAliexpress(navega):
    global produto,indiceproduto
    time.sleep(4)
    tamanho = 1

    veri = True

    divImg = 1
    while veri == True:
            try:
                images = navega.find_element(by=By.XPATH,value=f'/html/body/div[6]/div/div[2]/div/div[1]/div/div/div[{divImg}]/ul/li[{tamanho}]/div/img')
                image_pequena = images.get_attribute('src')
                url_grande = image_pequena.replace(".jpg_50x50", ".jpg_Q90").replace("_.webp", "")
                folder_path = Path(f"Produtos/{produto}{indiceproduto}/images")
                folder_path.mkdir(parents=True, exist_ok=True)
                path = folder_path / f"image{tamanho}.jpg"
                #print(url_grande)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(url_grande, headers=headers)
                open(path, 'wb').write(response.content)
                tamanho +=1
            except NoSuchElementException as e:
                #print(e)
                divImg += 1
                if divImg > 10:
                    veri = False
                #print(f"tamanho maximo de {tamanho}")
            except Exception as e:
                veri = False
                print(e)
                pass

    #input("Final baixar aliexpr")
    navega.close()





def buscarAliexpress(navegador):
    global produto,indiceproduto
    time.sleep(4)
    # encontra o drop down dos locais de envio
    drop_local = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[3]/div/div[2]/div[4]/div/a')
    try:
        drop_local.click()
    except:
        drop_local.click()
    print("Encontrou o dropdown dos locais")
    time.sleep(2)
    # abre seção para locais
    drop_local_sec = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[3]/div/div[2]/div[4]/div/div/div/div[1]/div')
    time.sleep(2)
    try:
        drop_local_sec.click()
    except:
        drop_local_sec.click()
    print("abriu seção dos locais")
    # place holder para colocar a localização
    place_holder_locals = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[3]/div/div[2]/div[4]/div/div/div/div[1]/div/div[1]/div/input')
    time.sleep(2)
    try:
        place_holder_locals.click()
    except:
        place_holder_locals.click()
    time.sleep(2)
    place_holder_locals.send_keys(local_envio)
    print("enviou local")
    # seleciona Brasil como local de envio
    drop_brazil_select = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[3]/div/div[2]/div[4]/div/div/div/div[1]/div/div[1]/ul/li[31]')
    time.sleep(2)
    try:
        drop_brazil_select.click()
    except:
        drop_brazil_select.click()
    print("selecionou o local")
    time.sleep(2)
    bt_filtrar = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[3]/div/div[2]/div[4]/div/div/div/div[5]/button')
    time.sleep(2)
    try:
        bt_filtrar.click()
    except:
        bt_filtrar.click()
    print("clicou em filtrar")
    time.sleep(3)
    place_holder_busca = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[4]/div/div[3]/form/div[2]/input')
    time.sleep(3)
    try:
        place_holder_busca.click()
    except:
        place_holder_busca.click()
    print("clicou no place holder do produto")
    time.sleep(2)
    produto = input("Qual produto voce deseja buscar ? ")
    #produto = "fone auricular bluetooth"
    place_holder_busca.send_keys(produto)
    print("escreveu o produto")
    time.sleep(3)
    bt_buscar_produto = navegador.find_element(by=By.XPATH,value='/html/body/div[3]/div[4]/div/div[3]/form/div[1]/input')
    try:
        bt_buscar_produto.click()
    except:
        bt_buscar_produto.click()
    print("buscou o produto")
    time.sleep(4)
    #seleciona os produtos com mais pedidos
    bt_pedidos = navegador.find_element(by=By.XPATH,value='/html/body/div[5]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div[2]')
    time.sleep(5)
    try:
        bt_pedidos.click()
    except:
        bt_pedidos.click()
    print("definiu com os mais pedidos")
    time.sleep(4)
    #define o produto inicial
    indiceproduto = 1
    qntsprod = int(input("Quantos produtos deseja buscar ? ")) + 1
    #ciclo para buscar quantos produtos quiser
    while indiceproduto < qntsprod:
        produto0 = navegador.find_element(by=By.XPATH,value=f'/html/body/div[5]/div/div/div[2]/div/div[2]/div[3]/a[{indiceproduto}]')

        #print(produto0.get_attribute('href'))
        print("-------------------------------------------------------")
        print(produto0.text)
        print("-------------------------------------------------------")
        path = f"Produtos/{produto}{indiceproduto}/"

        os.mkdir(path)
        path2 = f"Produtos//{produto}{indiceproduto}//images"
        os.mkdir(path2)
        with open(f"Produtos/{produto}{indiceproduto}/sobreoproduto.txt","w") as file:
            time.sleep(1)
            print("escrito descrição")
            file.write(f'''
            Descrição
            {produto0.text}
            \n
            \n
            Site do produto
            \n
            \n
            {produto0.get_attribute('href')}''')
            file.close()
        abrirNavegador(produto0.get_attribute('href'), "down")
        indiceproduto += 1
    #input("final buscar")


abrirNavegador(sites[0],"busca")