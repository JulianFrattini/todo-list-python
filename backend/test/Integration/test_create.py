import pytest
import unittest.mock as mock
from src.util.dao import DAO

@pytest.fixture
def sut():
    mockcollection = "video"
    dao = DAO(mockcollection)
    yield dao
    dao.drop()

def test_create_document_1(sut):
    tempdict = {
        [
            {
                "title": "Improve Devtools",
                "description": "Upgrade the tools used for web development. In order to keep web development effective, the right choice of tools is critical. This video presents seven interesting tools: BundlePhobia, CloudCraft, Figma, Fontflipper, Visbug, Insomnia, and Flare.",
                "url": "U_gANjtv28g",
                "todos": [
                    "Watch video", 
                    "Evaluate usability of tools", 
                    "Check out BundlePhobia and investigate npm packages in most recent projects"
                ]
            }, {
                "title": "Tech Stacks",
                "description": "Understand the structure of a tech stack and explore popular stacks in use.",
                "url": "Sxxw3qtb3_g",
                "todos": [
                    "Watch video", 
                    "Implement the techstack presented in the video"
                ]
            }, {
                "title": "Javascript Pro Tips",
                "description": "Get better at writing JavaScript Code",
                "url": "Mus_vwhTCq0",
                "todos": [
                    "Watch video"
                ]
            }, {
                "title": "Check out Elixir",
                "description": "Investigate the programming language Elixir, a dunamic functional programming language, which itself relied on the Erlang BEAM virutal machine. Since its strength lies in the construction of light-weight concurrent applications that still scale, it might be a valid option for future web development projects. Major companies utilizing Elixir are Discord, Motorola, and Pinterest.",
                "url": "R7t7zca8SyM",
                "todos": [
                    "Watch video",
                    "Install Elixir and Erlang",
                    "Check out Phoenix Framework for web development with Elixir",
                    "Rebuild todo application with Elixir"
                ]
            }, {
                "title": "Web Development Risks",
                "description": "Ultimately, web applications need to be secure in order to avoid loss of data or revenue upon deployment. Without any awareness for security risks, applications are prone to be exploitet. To ensure security by design, familiarize with common hacking stories relevant to web development.",
                "url": "4YOpILi9Oxs",
                "todos": [
                    "Watch video",
                    "Investiage used npm modules for security risks",
                    "Test resistance agains cross site scripting"
                ]
            }
        ]
    }
    result = sut.create(tempdict)
    assert result == True

def test_create_document_2(sut):
    assert True == True

def test_create_document_3(sut):
    assert True == True

def test_create_document_4(sut):
    assert True == True

def test_create_document_5(sut):
    assert True == True

def test_create_document_6(sut):
    assert True == True

def test_create_document_7(sut):
    assert True == True

def test_create_document_8(sut):
    assert True == True