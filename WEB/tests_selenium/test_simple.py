from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_forneinjet():
    # Configurar driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    
    try:
        # Testar página inicial
        driver.get("http://localhost:8080/SA_ForneInjet/WEB/")
        print("Página inicial carregada")
        
        # Testar navegação
        links = ["Clientes", "Fornecedores", "Injetoras", "Funcionários", "Vendas"]
        
        for link_text in links:
            try:
                link = driver.find_element(By.LINK_TEXT, link_text)
                link.click()
                print(f"Página {link_text} carregada com sucesso")
                time.sleep(1)
                driver.back()
            except Exception as e:
                print(f"Erro ao acessar {link_text}: {e}")
        
        # Testar adição de funcionário
        driver.get("http://localhost:8080/SA_ForneInjet/WEB/funcionarios.php")
        driver.find_element(By.NAME, "nome").send_keys("Teste Selenium")
        driver.find_element(By.NAME, "cargo").send_keys("Testador")
        driver.find_element(By.NAME, "telefone").send_keys("(11) 99999-9999")
        driver.find_element(By.NAME, "email").send_keys("teste@selenium.com")
        driver.find_element(By.NAME, "usuario").send_keys("teste.selenium")
        driver.find_element(By.NAME, "senha").send_keys("senha123")
        driver.find_element(By.NAME, "add").click()
        print("Funcionário adicionado")
        
        time.sleep(2)
        
    finally:
        driver.quit()
        print("Teste concluído")

if __name__ == "__main__":
    test_forneinjet()