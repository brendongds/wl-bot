import os
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from PIL import Image
import tempfile

client = commands.Bot(command_prefix="|",
                      intents=discord.Intents.all())




#################### variavel do questionario aqui----------------------

questions = [
    {"pergunta": "O que é RDM?", "alternativas": ["A) Atropelar com cavalo/carroça.\n", "B) Fazer coisas impossíveis de serem feitas na vida real.\n", "C) Matar sem gerar RP / sem motivos.\n", "D) Não se importar com a vida do personagem.\n"], "resposta": "C"},
    {"pergunta": "O que é HDM?", "alternativas": ["A) Atropelar com cavalo/carroça.\n", "B) Fazer coisas impossíveis de serem feitas na vida real.\n", "C) Matar sem gerar RP / sem motivos.\n", "D) Não se importar com a vida do personagem.\n"], "resposta": "A"},
    {"pergunta": "Você foi desmaiado por alguém, o que você faz logo que voltar do desmaio?", "alternativas": ["A) Vou juntar a galera e cobrar aquela pessoa que me desmaiou.\n", "B) Não posso fazer nada, pois como desmaiei não posso lembrar quem fez isso comigo.\n", "C) Subo suporte pois não aceito perder a ação.\n", "D) Saio contando pra todo mundo o que aconteceu e espero que alguém mate o cara por mim.\n"], "resposta": "B"},
    {"pergunta": "Um grupo de 6 pessoas armadas encontra você e pede para que se renda, o que você faz?", "alternativas": ["A) Deslogo do jogo para não perder meus itens.\n", "B) Levanto a mão para que eles pensem que me rendi e começo a atirar neles logo após isso.\n", "C) Me faço de surdo e aviso meus amigos para me ajudar.\n", "D) Levanto as mãos e sigo o RP.\n"], "resposta": "D"},
    {"pergunta": "Você está vendo a live de alguém e descobre uma fofoca sobre sobre o RP:", "alternativas": ["A) Não posso levar essa informação pra dentro do RP pois vi em live.\n", "B) Falo para todo mundo.\n", "C) Não conto para ninguém mas uso a informação para me favorecer ingame.\n", "D) Vou correndo encontrar o streamer no RP para que meu personagem fique sabendo da fofoca.\n"], "resposta": "A"},
    {"pergunta": "Um oficial está vendo um suspeito próximo e não dá tempo de chamar reforços, ele resolve pedir ajuda para você, como você agiria?", "alternativas": ["A) Não posso ajudar pois não sou oficial.\n", "B) Se eu quiser, eu posso ajudar, pois a lei me permite auxiliar em casos específicos se algum oficial precisar.\n", "C) Pediria dinheiro em troca da minha ajuda.\n", "D) Ajudaria o oficial mas assumiria o controle da situação.\n"], "resposta": "B"},
    {"pergunta": "Quais horários são permitidos assaltos?", "alternativas": ["A) Não há restrição de horário.\n", "B) 19:00 às 07:00\n", "C) 06:00 às 18:00\n", "D) 18:00 às 06:00\n"], "resposta": "D"},
    {"pergunta": "Qual o contingente minimo para roubos menores? (Loja de armas, mercearia, Saloon, Mercado clandestino, Cemitérios) ", "alternativas": ["A) 1 bandido. \n", "B) 2 bandidos. \n", "C) 3 bandidos. \n", "D) Não existe regras sobre contingente minimo.\n"], "resposta": "A"},
    {"pergunta": "Para iniciar um roubo grande, roubo a bancos por exemplo, qual o contingente minimo permitido?", "alternativas": ["A) Minimo 3 bandidos e 3 oficiais.\n", "B) Minimo 4 bandidos e 4 oficiais.\n", "C) Minimo 6 bandidos e 6 oficiais.\n", "D) Minimo 8 bandidos e 8 oficiais.\n"], "resposta": "B"},
    {"pergunta": "Qual o máximo de NPCs que podem ser usados em roubos?", "alternativas": ["A) Não pode usar NPCs como refém. \n", "B) No máximo 1 refém em roubos menores e 2 em roubos maiores.\n", "C) No máximo 2 reféns em roubos menores e 3 em roubos maiores.\n", "D) Não há limites de reféns NPCs.\n"], "resposta": "B"},
]




@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.dnd,
                               activity=discord.Game("Alvorada RP"))
  print(
    "Bot online e status alterado para 'ocupado' com a frase 'Alvorada RP'."
  )

@client.event 
async def on_message(message):
    if message.channel.id == 1086172175033176146:
        await message.author.edit(nick=message.content)
        await message.add_reaction("✅")
        
    elif message.channel.id == 1086449132979372036 and message.author != client.user:
        await message.add_reaction("✅") 
        await message.add_reaction("❌")
        thread_name = message.content
        thread = await message.create_thread(name=message.content)
        await thread.send("Tópico criado", delete_after=1.0)
    
########## resize by diabetinho ###########
    
    if message.author == client.user:
      return
    if message.content.startswith('|resize'):
      if message.attachments:
        for attachment in message.attachments:
          if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.png'):
            extension = attachment.filename.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix="."+extension) as f:
              f.write(await attachment.read())
              f.seek(0)
              image = Image.open(f.name)
              image = image.resize((image.width * 7, image.height * 7))
              image.save(f.name)
              await message.channel.send(file=discord.File(f.name)) 
    

########### iniciar aqui --------------

    if message.channel.id == 1086173691957760010 and message.content.lower() == "iniciar": ##### substituir pelo ID do canal 'FAZER-AL' do ALVORADA - ok
        user_id = message.author.id
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = client.get_channel(1091127127811838002) ##### substituir pelo ID da aba 'WLS' do ALVORADA - ok
        channel_name = f"{message.author.name}-wl " 
        channel = await message.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        channel_id = channel.id

        await message.delete()
        await message.author.send(f"O seu formulário de WL foi criado em {channel.mention} <<< Você pode clicar para ser redirecionado.")
        
        ##### funções pra ocultar & mostrar canal de fazer-wl :
        async def ocultar_canal_wl(channel):
          channel = client.get_channel(1086173691957760010) ##### substituir pelo ID do canal 'FAZER-AL' do ALVORADA - ok
          await channel.set_permissions(message.guild.get_member(user_id), read_messages=False)
        await ocultar_canal_wl(channel)

        async def mostrar_canal_wl(channel):
          channel = client.get_channel(1086173691957760010) ##### substituir pelo ID do canal 'FAZER-AL' do ALVORADA - ok
          await channel.set_permissions(message.guild.get_member(user_id), read_messages=True, send_messages=True)

        ##### função pra apagar o canal de user-wl :
        async def apagar_canal(channel):
          channel = client.get_channel(channel_id)
          await asyncio.sleep(15) #### botei pra apagar o canal da wl em 15 segundos, tem q ver o que achar melhor, eu achei q ficou bom
          await channel.delete()
         
        #####

        embed = discord.Embed(title="Formulário de whitelist", description="Para iniciar a sua whitelist, recomendo que já tenha a história do seu personagem escrita de uma maneira breve, pois será necessário no final do formulário.\nTambém será necessário o conhecimento de nossas regras, que podem ser encontradas aqui: https://tinyurl.com/Alvorada-Regras\nO tempo limite para responder cada pergunta é de 120 segundos, caso não responda a tempo, o formulário será encerrado.\nQuando estiver pronto, clique no emote abaixo.")
        embed.set_footer(text="Alvorada Roleplay")
        msg = await channel.send(embed=embed)
        await msg.add_reaction("✅")


        def check(reaction, user):
          return reaction.message.id == msg.id and user != client.user

        while True:
          reaction, user = await client.wait_for('reaction_add', check=check)
          if reaction.emoji == "✅":
        

            num_questions = len(questions)
            current_question = 0
            user_answers = []
            
            for question in questions:
                current_question += 1
                await channel.send(f"**Pergunta {current_question} de {num_questions}:** {question['pergunta']}")
                await channel.send(f"{''.join(question['alternativas'])}") 
                def check(m):
                    return m.channel == channel and m.author == message.author
                while True:
                    answer = await client.wait_for('message', check=check)
                    if answer.content.upper() in ["A", "B", "C", "D"]:
                        user_answers.append(answer.content.upper())
                        await channel.purge(limit=3)
                        break
                    else:
                        await channel.purge(limit=1)
                        continue
            
            if current_question == num_questions:
                
                correct_answers = 0
                for i in range(num_questions):
                    if user_answers[i] == questions[i]['resposta']:
                        correct_answers += 1
                if correct_answers == num_questions:
                    await channel.purge(limit=None)  
                    await channel.send(f"Parabéns, {message.author.mention}! Você acertou todas as {num_questions} perguntas! Agora precisamos saber um pouco mais de você e de seu personagem, após o envio, aguarde alguem da Staff validar seus dados e história do personagem.")
                    # Pergunta 1
                    await channel.send("Qual seu nome e idade real?")
                    msg1 = await client.wait_for('message', check=lambda msg: msg.channel == channel and msg.author == message.author)

                    # Pergunta 2
                    await channel.send("Qual o nome e idade do seu personagem?")
                    msg2 = await client.wait_for('message', check=lambda msg: msg.channel == channel and msg.author == message.author)

                    # Pergunta 3
                    await channel.send("Tem experiência em servidores de RP? Se sim, há quanto tempo você joga?")
                    msg3 = await client.wait_for('message', check=lambda msg: msg.channel == channel and msg.author == message.author)

                    # Pergunta 4
                    await channel.send("Conte um pouco sobre seu personagem, como: de onde vem, personalidade, motivações, objetivos, habilidades e talentos.\nObs.: A mensagem não pode ter mais de 1000 caracteres. ")
                    
                    while True:
                      msg4 = await client.wait_for('message', check=lambda msg: msg.channel == channel and msg.author == message.author)
                      if len(msg4.content) > 1000:
                        await channel.send("Sua mensagem contém mais de 1000 caracteres. Por favor, reduza um pouco sua lore.")
                      else:
                        break


                    await channel.send("Seus dados foram enviados e você receberá a tag de <@&1086172608455774268> se for aprovado. Não se preocupe, não demora muito e você será notificado quando acontecer.")  ##### substituir pelo ID da tag 'AGUARDANDO ENTREVISTA' do ALVORADA - ok
                    await channel.set_permissions(message.guild.get_member(user_id), read_messages=True, send_messages=False)
                    
                    
                    respostas = [msg1.content, msg2.content, msg3.content, msg4.content]
                                        
                    
                    channel = client.get_channel(1087947833027592192) ##### substituir pelo ID do canal 'DADOS WL' ALVORADA - ok
                    await channel.send("---------------------------------------------------")
                    await channel.send(f'{client.get_user(user_id).mention}')
                    embed = discord.Embed(title=f"", color=0x00ff00)
                    embed.add_field(name="Nome e idade real", value=respostas[0], inline=False)
                    embed.add_field(name="Nome e idade do personagem", value=respostas[1], inline=False)
                    embed.add_field(name="Experiência em servidores de RP", value=respostas[2], inline=False)
                    embed.set_footer(text=f"--------------------\nWL de {message.author.name}")

                    await channel.send(embed=embed)

                    embed = discord.Embed(title="Lore:", color=0x00ff00)
                    embed.add_field(name="", value=respostas[3], inline=False)
                    embed.set_footer(text=f"--------------------\nWL de {message.author.name}")
                    await channel.send(embed=embed)

                    embed = discord.Embed(title="", color=0x00ff00)
                    embed.add_field(name="", value=f"✅ - Aprova o usuário.\n🧒 - Reprova por Idade.\n🪪 - Reprova por Nome do Personagem.\n📖 - Reprova por Lore.\n-----------------------------------------")
                    embed.set_footer(text=f"WL de {message.author.name}")
                    channel = client.get_channel(1087947833027592192) ##### substituir pelo ID do canal 'DADOS WL' ALVORADA - ok
                    
                    
                    msg = await channel.send(embed=embed)
                    await msg.add_reaction("✅")
                    await msg.add_reaction("🧒")
                    await msg.add_reaction("🪪")
                    await msg.add_reaction("📖")

                    asyncio.create_task(apagar_canal(channel))

                    def check(reaction, user):
                      return reaction.message.id == msg.id and user != client.user and user.guild_permissions.move_members

                    while True:
                      reaction, user = await client.wait_for('reaction_add', check=check)
                      if reaction.emoji == "✅":
                        users = await reaction.users().flatten()
                        await client.get_channel(1085841563554426931).send(f"{client.get_user(user_id).mention} foi aprovado na AllowList! Parabéns, aguarde a entrevista e seja bem-vindo.") ##### substituir pelo ID do canal 'APROVADOS' do ALVORADA - ok
                        server = client.get_guild(1085201225953325146) ##### substituir pelo ID do server do ALVORADA - ok
                        member = server.get_member(user_id) 
                        role = server.get_role(1086172608455774268) ##### substituir pelo ID da tag 'AGUARDANDO ENTREVISTA' do ALVORADA - ok
                        await member.add_roles(role)
                        role = server.get_role(1085201225953325151) ##### substituir pelo ID da tag 'FORASTEIRO' do ALVORADA - ok
                        await member.remove_roles(role)                       

                      elif reaction.emoji == "🧒":
                        users = await reaction.users().flatten()
                        await client.get_channel(1085841613357600828).send(f"{client.get_user(user_id).mention} reprovou na AllowList. Menores de idade não são permitidos no servidor.") ##### substituir pelo ID do canal 'REPROVADOS' do ALVORADA - ok
                        
                      elif reaction.emoji == "🪪":
                        users = await reaction.users().flatten()
                        await client.get_channel(1085841613357600828).send(f"{client.get_user(user_id).mention} reprovou na AllowList. Por favor revise o nome do seu personagem, consulte as regras para saber o que é permitido ou não: <#1085685438834032691>") ##### substituir o primeiro pelo ID do canal 'REPROVADOS' e o segundo pelo 'REGRAS DO SV' do ALVORADA - ok
                        await mostrar_canal_wl(channel)

                      elif reaction.emoji == "📖":
                        users = await reaction.users().flatten()
                        await client.get_channel(1085841613357600828).send(f"{client.get_user(user_id).mention} reprovou na AllowList. Sua lore foi reprovada, por favor de-nôs mais detalhes sobre seu personagem na próxima vez.") ##### substituir pelo ID do canal 'REPROVADOS' do ALVORADA - ok 
                        await mostrar_canal_wl(channel)


                else:
                  await channel.purge(limit=None)  
                  await channel.send(f"{message.author.mention}, você acertou {correct_answers} de {num_questions} perguntas. Infelizmente, você foi reprovado.\n Mas não desanime, você pode tentar novamente.")
                  await channel.set_permissions(message.guild.get_member(user_id), read_messages=True, send_messages=False)
                  await client.get_channel(1085841613357600828).send(f"{message.author.mention} reprovou na AllowList, acertou {correct_answers} das {num_questions} perguntas.") ##### substituir pelo ID do canal 'REPROVADOS' do ALVORADA - ok
                  await mostrar_canal_wl(channel)
                  await apagar_canal(channel)

    elif message.channel.id == 1086173691957760010 and message.content.lower() != "iniciar": ##### substituir pelo ID do canal 'FAZER-AL' do ALVORADA - ok
      await message.delete()
    
    
    await client.process_commands(message)





@client.command()
async def enviar(ctx, *, mensagem):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.message.delete()
        await ctx.send(mensagem)
    else:
        await ctx.message.delete()
        
@client.command(name='Patchnotes') 
@commands.has_permissions(administrator=True)
async def patchnotes(ctx):
    await ctx.message.delete()

    author = ctx.author
    dm_channel = await author.create_dm()
    await dm_channel.send("Qual a versão da atualização? Exemplo: v1.2.1")

    def check_author(m):
        return m.author == author and isinstance(m.channel, discord.DMChannel)

    version_message = await client.wait_for('message', check=check_author)
    version = version_message.content
    await dm_channel.send(f"Atualizões {version}. Mande a lista de atualizações.")

    text_message = await client.wait_for('message', check=check_author)
    text = text_message.content

    embed = discord.Embed(title=f"Atualização {version}", description=text, color=discord.Color.gold())
    embed.set_footer(text="Alvorada Roleplay", icon_url="https://i.imgur.com/lgWBe3X.png")
    embed.set_thumbnail(url="https://i.imgur.com/lgWBe3X.png")
    embed.add_field(name="\u200b", value=f"<@&1085201225953325154>")

    channel = client.get_channel(1085201227370999936)
    await ctx.channel.send(f"||<@&1085201225953325154>||")
    await channel.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def anuncio(ctx, *, mensagem):
    embed = discord.Embed(description=mensagem, color=discord.Color.red())
    embed.set_footer(text="Alvorada Ropleplay", icon_url="https://i.imgur.com/lgWBe3X.png")
    await ctx.message.delete()
    await ctx.send(embed=embed)

@anuncio.error
async def anuncio_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()





################# STATUS DO BOT #################


@client.command()  
async def transmitindo(ctx, stream_name: str):
  if ctx.author.id != 608069911763222548:
    await ctx.message.delete()
    return
  await client.change_presence(activity=discord.Streaming(
    name=stream_name, url="https://www.twitch.tv/yelloxbr"))
  await ctx.message.delete()


@client.command()  
async def ouvindo(ctx, music_name: str):
  if ctx.author.id != 608069911763222548:
    await ctx.message.delete()
    return
  await client.change_presence(status=discord.Status.dnd,
                               activity=discord.Activity(
                                 type=discord.ActivityType.listening,
                                 name=music_name))
  await ctx.message.delete()

  
@client.command()  
async def competindo(ctx, competing_name: str):
  if ctx.author.id != 608069911763222548:
    await ctx.message.delete()
    return
  await client.change_presence(status=discord.Status.dnd,
                               activity=discord.Activity(
                                 type=discord.ActivityType.competing,
                                 name=competing_name))
  await ctx.message.delete()


@client.command()  
async def jogando(ctx, game_name: str):
  if ctx.author.id != 608069911763222548:
    await ctx.message.delete()
    return
  await client.change_presence(status=discord.Status.dnd,
                               activity=discord.Activity(
                                 type=discord.ActivityType.playing,
                                 name=game_name))
  await ctx.message.delete()


@client.command()  
async def assistindo(ctx, assistindo_name: str):
  if ctx.author.id != 608069911763222548:
    await ctx.message.delete()
    return
  await client.change_presence(status=discord.Status.dnd,
                               activity=discord.Activity(
                                 type=discord.ActivityType.watching,
                                 name=assistindo_name))
  await ctx.message.delete()

####################################### TESTES PARA WL #######################################
 
titulo = "Bem-vindo ao servidor Alvorada RP"
mensagem = """
Para iniciar a sua whitelist, recomendo que já tenha a história do seu personagem escrita de uma maneira breve, pois será necessário no final do formulário.\n
Também será necessário o conhecimento de nossas regras, que podem ser encontradas aqui:
https://tinyurl.com/Alvorada-Regras
O tempo limite para responder cada pergunta é de 120 segundos, caso não responda a tempo, o formulário será encerrado.\n
**Quando estiver pronto, escreva "iniciar" para começar a sua wl.**
"""
cor = discord.Color(0xFFFFFF) 
imagem = "https://i.imgur.com/lgWBe3X.png" # URL da imagem para usar no corpo do embed
rodape = "Alvorada RP"

@client.command()
async def msgwl(ctx):
    if ctx.author.id == 608069911763222548:
        embed = discord.Embed(title=titulo, description=mensagem, color=cor)
        embed.set_thumbnail(url=imagem)
        embed.set_footer(text=rodape, icon_url=imagem)
        await ctx.send(embed=embed)


client.remove_command('help')
@client.command()
async def comandos(ctx):
    embed = discord.Embed(title="Comandos do BOT", description="Comandos de chat:\n|comandos - Mostra essa mensagem\n|resize - Dá zoom em uma parte da imagem.\n|enviar - Bot reenvia a mensagem do usuário no mesmo canal. (adm)\n|patchnotes - Bot chama na DM e pergunta as atualizações. (adm)\n|anuncio - Bot envia mensagem com um embed vermelho no mesmo canal. (adm)\n|jogando - Muda o status do bot para jogando [texto]. (yLx)\n|ouvindo - Muda o status do bot para ouvindo [texto]. (yLx)\n|assistindo - Muda o status do bot para assistindo [texto]. (yLx)\n|competindo - Muda o status do bot para competindo [texto]. (yLx)\n|transmitindo - Muda o status do bot para transmitindo [texto]. (yLx)\n|msgwl - Manda a mensagem padrão no canal de WL. (yLx)\n\nOutras funções:\n- Altera o nome dos usuários quando enviado em um canal específico.\n- Cria tópico nas mensagens enviadas no canal de sugestão e coloca reações.\n- Sistema de WL interativo e \"automático\":\nO usuário envia uma mensagem no canal para fazer WL e o bot cria uma sala privada com ele para fazer as perguntas. Caso acerte todas as perguntas, o bot coleta alguns dados como: Nome e idade real e do personagem, tempo de experiência em RP e um resumo da lore do personagem, e depois envia no canal de \"dados\" com alguns emotes. Cada emote com uma função diferente, podendo aprovar o usuário (ele perde o cargo de \"Forasteiro\" e recebe o cargo de \"Aguardando entrevista\") e outros 3 emotes variando o motivo das reprovações, sendo eles: reprovar por idade, nome do personagem ou lore. Caso erre 1 ou mais perguntas da WL, o usuário é reprovado automaticamente.\nObs.: Sempre que alguém for aprovado ou reprovado, é enviada uma mensagem nos canais correspondentes marcando o usuário.", color=0xFED500)
    embed.set_footer(text="Alvorada Rolimpas", icon_url=imagem)
    await ctx.send(embed=embed)

@client.command()
async def online(ctx):
  await ctx.send("wl - online")


################



with open("token.0", "r", encoding="utf-8") as f:
  AlvoradaRPbot = f.read()
client.run(AlvoradaRPbot)
