from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest

class TestForneInjet:
    @classmethod
    def setup_class(cls):
        """Configuração inicial antes de todos os testes"""
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost/SA_ForneInjet/WEB/"  # Altere para a URL do seu servidor
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def teardown_class(cls):
        """Limpeza após todos os testes"""
        cls.driver.quit()
    
    
    def test_01_acessar_pagina_inicial(self):
        """Testa acesso à página inicial"""
        self.driver.get(self.base_url)
        # Verifica se o título contém "ForneInjet"
        assert "ForneInjet" in self.driver.title
        # Verifica se elementos da página estão presentes
        assert "Painel Administrativo" in self.driver.page_source
        assert "Clientes" in self.driver.page_source
    
    def test_02_navegar_para_funcionarios(self):
        """Testa navegação para a página de funcionários"""
        self.driver.get(self.base_url)
        link_funcionarios = self.driver.find_element(By.LINK_TEXT, "Funcionários")
        link_funcionarios.click()
        
        assert "Gerenciar Funcionários" in self.driver.page_source
        assert "Adicionar" in self.driver.page_source
    
    def test_03_adicionar_novo_funcionario(self):
        """Testa adição de novo funcionário"""
        self.driver.get(f"{self.base_url}/funcionarios.php")
        
        # Preencher formulário
        self.driver.find_element(By.NAME, "nome").send_keys("João Silva Teste")
        self.driver.find_element(By.NAME, "cargo").send_keys("Analista de Testes")
        self.driver.find_element(By.NAME, "telefone").send_keys("(11) 99999-9999")
        self.driver.find_element(By.NAME, "email").send_keys("joao.teste@email.com")
        self.driver.find_element(By.NAME, "usuario").send_keys("joao.teste")
        self.driver.find_element(By.NAME, "senha").send_keys("senha123")
        
        # Clicar em adicionar
        self.driver.find_element(By.NAME, "add").click()
        
        # Verificar se o funcionário foi adicionado na tabela
        time.sleep(2)  # Aguardar carregamento
        assert "João Silva Teste" in self.driver.page_source
    
    def test_04_adicionar_novo_cliente(self):
        """Testa adição de novo cliente"""
        self.driver.get(f"{self.base_url}/clientes.php")
        
        # Preencher formulário
        self.driver.find_element(By.NAME, "nome").send_keys("Empresa Teste Ltda")
        self.driver.find_element(By.NAME, "cnpj").send_keys("12.345.678/0001-00")
        self.driver.find_element(By.NAME, "telefone").send_keys("(11) 8888-8888")
        self.driver.find_element(By.NAME, "email").send_keys("contato@empresateste.com")
        
        # Clicar em adicionar
        self.driver.find_element(By.NAME, "add").click()
        
        # Verificar se o cliente foi adicionado
        time.sleep(2)
        assert "Empresa Teste Ltda" in self.driver.page_source
    
    def test_05_adicionar_nova_injetora(self):
        """Testa adição de nova injetora"""
        self.driver.get(f"{self.base_url}/injetoras.php")
        
        # Preencher formulário
        self.driver.find_element(By.NAME, "marca").send_keys("Marca Teste")
        self.driver.find_element(By.NAME, "modelo").send_keys("Modelo X")
        self.driver.find_element(By.NAME, "tipo").send_keys("Elétrica")
        self.driver.find_element(By.NAME, "capacidade").send_keys("200")
        self.driver.find_element(By.NAME, "forca").send_keys("500")
        self.driver.find_element(By.NAME, "preco").send_keys("100000")
        self.driver.find_element(By.NAME, "quantidade").send_keys("5")
        
        # Clicar em adicionar
        self.driver.find_element(By.NAME, "add").click()
        
        # Verificar se a injetora foi adicionada
        time.sleep(2)
        assert "Marca Teste" in self.driver.page_source
    
    def test_06_testar_exclusao_item(self):
        """Testa exclusão de um item (funcionário)"""
        self.driver.get(f"{self.base_url}/funcionarios.php")
        
        # Encontrar todos os links de exclusão
        delete_links = self.driver.find_elements(By.LINK_TEXT, "Excluir")
        
        if delete_links:
            # Clicar no primeiro link de exclusão
            delete_links[0].click()
            
            # Confirmar alerta (se houver)
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
            
            time.sleep(2)
            print("Item excluído com sucesso")
    
    def test_07_testar_navegacao_completa(self):
        """Testa navegação por todas as páginas"""
        pages = [
            ("Clientes", "clientes.php", "Gerenciar Clientes"),
            ("Fornecedores", "fornecedores.php", "Gerenciar Fornecedores"),
            ("Injetoras", "injetoras.php", "Gerenciar Injetoras"),
            ("Vendas", "vendas.php", "Gerenciar Vendas")
        ]
        
        for page_name, page_url, expected_text in pages:
            self.driver.get(f"{self.base_url}/{page_url}")
            assert expected_text in self.driver.page_source
            print(f"Página {page_name} carregada com sucesso")
    
    def test_08_testar_formularios_vazios(self):
        """Testa envio de formulários vazios"""
        self.driver.get(f"{self.base_url}/funcionarios.php")
        
        # Tentar enviar formulário vazio
        self.driver.find_element(By.NAME, "add").click()
        
        # Verificar se a página ainda está carregada (não quebrou)
        assert "Gerenciar Funcionários" in self.driver.page_source

# Para executar os testes
if __name__ == "__main__":
    pytest.main([__file__, "-v"])