# Tenofit Checkin
- Checkins automáticos no app tecnofit box.
- Sempre que o código é executado, ele realiza o checkin automaticamente no horário escolhido do dia seguinte.

# Como Usar
## Passo 1 - Obter o token
- Para obter o token, você deve executar o arquivo **get_token.py**
- Substitua a variável *USER* pelo seu e-mail de login e a variável *PASSWORD* pela sua senha (linhas 
- Uma lista com os nomes dos boxes no qual você tem conta ativa irá aparecer com os respectivos tokens de cada um. Copie o Token do box de sua escolha.

## Passo 2 - Programar o checkin
- Para realizar o checkin, você deve executar o arquivo **scheduler.py** 
- Altere a variável *TOKENS* da linha 17 para uma tupla com os tokens desejados. Cada dicionário da tupla corresponde a uma pessoa diferente e deve conter as 3 propriedades:
  - nome: apenas para identificar a pessoa que o checkin está sendo realizado para ficar registrado nos logs de execução
  - token: o token da pessoa que terá o checkin realizado. O token deve ser obtido seguindo o Passo 1
  - hora_checkin: horário desejado para o checkin. O horário deve estar no formato HH:mm (e.x.: 06:00, 17:00, 12:30)
- Execute o código. O checkin será realizado para o dia seguinte e, caso haja pesquisas pendentes de respostas, ele tentará responder
- O ideal é agendar para que o código seja executado assim que o checkin é liberado
