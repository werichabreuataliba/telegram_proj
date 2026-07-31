clinica_medica ={
  "especialidade": "CLINICA_MEDICA",

  "categoria": "DOENCA_CRONICA",

  "steps": [

    {
      "step": 1,

      "pergunta":
      "Você é o paciente ou responsável pelo paciente?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 2
    },

    {
      "step": 2,

      "pergunta":
      "Está utilizando os medicamentos prescritos diariamente?",

      "opcoes": [
        "Sim",
        "Não",
        "Às vezes"
      ],

      "proximo_step": 3
    },

    {
      "step": 3,

      "pergunta":
      "Mediu sua pressão arterial nos últimos dias?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 4
    },

    {
      "step": 4,

      "pergunta":
      "Apresentou dor de cabeça ou tontura?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 999
    }

  ]
}

pediatria = {
  "especialidade": "PEDIATRIA",

  "categoria": "ACOMPANHAMENTO_PEDIATRICO",

  "steps": [

    {
      "step": 1,

      "pergunta":
      "Você é o responsável pela criança?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 2
    },

    {
      "step": 2,

      "pergunta":
      "A criança apresentou febre?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 3
    },

    {
      "step": 3,

      "pergunta":
      "Precisou utilizar medicação de resgate?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 4
    },

    {
      "step": 4,

      "pergunta":
      "A criança está conseguindo brincar normalmente?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 999
    }

  ]
}

cardiologia = {
  "especialidade": "CARDIOLOGIA",

  "categoria": "POS_EVENTO_CARDIACO",

  "steps": [

    {
      "step": 1,

      "pergunta":
      "Você é o paciente ou responsável pelo paciente?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 2
    },

    {
      "step": 2,

      "pergunta":
      "Após a alta hospitalar apresentou dor no peito?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 3
    },

    {
      "step": 3,

      "pergunta":
      "Está utilizando os medicamentos prescritos?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 4
    },

    {
      "step": 4,

      "pergunta":
      "Conseguiu marcar retorno com o cardiologista?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 5
    },

    {
      "step": 5,

      "pergunta":
      "Apresentou falta de ar ou inchaço nas pernas?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 999
    }

  ]
}

psiquiatria = {
  "especialidade": "PSIQUIATRIA",

  "categoria": "SAUDE_MENTAL",

  "steps": [

    {
      "step": 1,

      "pergunta":
      "Você é o paciente ou responsável?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 2
    },

    {
      "step": 2,

      "pergunta":
      "Está tomando a medicação conforme orientação médica?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 3
    },

    {
      "step": 3,

      "pergunta":
      "Percebe melhora dos sintomas emocionais?",

      "opcoes": [
        "Sim",
        "Parcialmente",
        "Não"
      ],

      "proximo_step": 4
    },

    {
      "step": 4,

      "pergunta":
      "Está frequentando as sessões de terapia?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 5
    },

    {
      "step": 5,

      "pergunta":
      "Apresentou efeitos colaterais da medicação?",

      "opcoes": [
        "Sim",
        "Não"
      ],

      "proximo_step": 999
    }

  ]
}





