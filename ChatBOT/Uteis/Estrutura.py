from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
)
from langchain.chains import (
    RetrievalQA
)
import json


patient_sessions = {}

def extract_patient_data(user_id, vectorstores):

    vectorstore = vectorstores[user_id]

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    docs = vectorstore.similarity_search(
        "Nome do paciente",
        k=10
    )

    for doc in docs:
        print("========== DOCUMENTO ==========")
        print(doc.page_content)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    prompt = """
    Você é um especialista em interpretação de prontuários médicos.

Sua tarefa é analisar o prontuário e extrair informações estruturadas.

IMPORTANTE:

- Retorne APENAS um JSON válido.
- Nunca escreva explicações.
- Nunca utilize Markdown.
- Nunca envolva o JSON com ```json.
- Não invente informações.
- Caso um campo não exista, retorne "".

A especialidade deve ser classificada APENAS entre as opções abaixo:

- CLINICA_MEDICA
- CARDIOLOGIA
- PSIQUIATRIA
- PEDIATRIA

A categoria NÃO deve ser copiada do documento.

Ela deve ser CLASSIFICADA utilizando APENAS uma das opções abaixo:

- DOENCA_CRONICA
- POS_EVENTO_CARDIACO
- SAUDE_MENTAL
- ACOMPANHAMENTO_PEDIATRICO

Utilize o diagnóstico, procedimento e contexto clínico para escolher a categoria mais adequada.

Caso nenhuma categoria represente corretamente o prontuário, retorne:

"categoria":"OUTROS"

Retorne exatamente neste formato:

{
    "nome":"",
    "idade":"",
    "sexo":"",
    "diagnostico":"",
    "retorno":"",
    "especialidade":"",
    "categoria":""
}
    """


    # prompt = """
    #     Analise o prontuário e retorne APENAS um JSON.
    #     {
    #      "nome":"",
    #      "idade":"",
    #      "sexo":"",
    #      "diagnostico":"",
    #      "retorno":"",
    #      "especialidade": "",
    #      "categoria": ""
    #     }
    # """

    return json.loads(qa.run(prompt))


async def etapas(step, question, session, update):
    if step == 1:

        if question == "1":

            session["step"] = 2

            await update.message.reply_text(
                """
                Desde a cirurgia você percebeu melhora da visão?
            
                1 - Sim
                2 - Parcialmente
                3 - Não
                """
            )

            return

        else:

            await update.message.reply_text(
                "Atendimento encerrado."
            )

            return

    if step == 2:
        session["respostas"][
            "melhora_visao"
        ] = question

        session["step"] = 3

        await update.message.reply_text(
            """
            Está utilizando corretamente os medicamentos prescritos?
        
            1 - Sim
            2 - Não
            """
        )

        return

    if step == 3:
        session["respostas"][
            "medicacao"
        ] = question

        session["step"] = 4

        await update.message.reply_text(
            """
            Está sentindo algum dos sintomas abaixo?
        
            1 - Dor ocular
        
            2 - Vermelhidão
        
            3 - Visão embaçada
        
            4 - Nenhum
            """
        )

        return

    if step == 4:
        session["respostas"][
            "sintomas"
        ] = question

        session["step"] = 5

def generate_summary(session):

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    prompt = f"""
Você é um médico especialista responsável pela triagem de pacientes.

Sua tarefa é analisar o quadro clínico utilizando:

1. O diagnóstico extraído do prontuário.
2. Os dados do paciente.
3. As respostas fornecidas durante a entrevista.

Dados do paciente

Nome: {session['nome']}
Idade: {session['idade']}
Sexo: {session['sexo']}
Diagnóstico: {session['diagnostico']}
Retorno previsto: {session['retorno']}

Respostas da entrevista

{json.dumps(session['respostas'], indent=2, ensure_ascii=False)}

Com base nessas informações elabore um relatório contendo exatamente as seguintes seções:

## Resumo Clínico
Faça um breve resumo do caso.

## Análise Clínica
Explique o que as respostas do paciente indicam em relação ao diagnóstico existente.

## Prognóstico
Descreva a evolução clínica mais provável considerando as informações disponíveis.

## Classificação de Risco
Classifique o caso como:

- Baixo
- Moderado
- Alto

Explique por que essa classificação foi escolhida.

## Conduta Recomendada
Informe a orientação mais adequada entre:

- Manter acompanhamento de rotina;
- Antecipar consulta médica;
- Encaminhar para avaliação urgente.

Importante:

- Não invente informações.
- Baseie-se apenas nos dados recebidos.
- Caso as informações sejam insuficientes, deixe isso explícito.
- O texto deve ser técnico, claro e objetivo.
- Não utilize Markdown nem emojis.
"""

    return llm.invoke(prompt).content
# def generate_summary(
#     session
# ):
#
#     llm = ChatOpenAI(
#         model="gpt-3.5-turbo",
#         temperature=0
#     )
#
#     prompt = f"""
# Você é uma assistente médica.
#
# Analise o quadro clínico do paciente considerando o diagnóstico extraído do prontuário e
# todas as respostas fornecidas durante a triagem. Elabore um prognóstico, classifique o risco (baixo/médio/alto),
# justifique a classificação e informe se há necessidade de contato imediato com a equipe médica ou
#  apenas manutenção do acompanhamento.
#
# Paciente:
# {session['nome']}
#
# Idade:
# {session['idade']}
#
# Diagnóstico:
# {session['diagnostico']}
#
# Respostas:
# {session['respostas']}
# """
#
#     return (
#         llm.invoke(prompt)
#         .content
#     )