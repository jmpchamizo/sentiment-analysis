# Sentiment Analysis
## Proyecto
<p>Implementación de una api que permita la creación de una base de datos (en MongoDB) de usuarios, mensajes y chats y analice el contenido de estos chats para después recomendar a usuarios a otros usuarios en función del contenido de sus mensajes, también recomendará por chat otros chats por el contenido de estos y por último ofrecerá chats a los usuarios comparando los sentimientos de los mensajes de los usuarios en función de los sentimientos de los chats.</p>

## Contenido en las carpetas
<p>En la carpeta Input/ esta la carpeta dumps con la bbdd analysis con las colecciones que corresponden a dialogos de la serie Battlestar Gallactica sacados de la web https://www.tv-quotes.com/shows/battlestar-galactica-2003.html</p>
<p>Para cargar la bbdd en local desde la carpeta Input/:</p>
<pre><code>mongorestore --uri="mongodb://localhost/analysis"</code></pre>
<p>En la carpeta src/chat, además hay un chat en js básico para visualizar el contenido de los chat según el usuario. También se puede dar de alta usuarios, chats y mensajes desde ahi como un ejemplo de uso de la api</p>
<p>El chat no esta finalizado produciendo errores si se introducen usuarios que no tengan chats, ni mensajes.</p>

## Descripción de la api
<p>Endpoints:</p>
<pre><code>/user/create/[username]</code></pre>
<p>Permite crear un usuario:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: username (nombre del usuario)</li>
    <li>Return: user_id</li>
</ul>
<pre><code>/chat/create/[chatname]</code></pre>
<p>Permite crear un chat:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: chatname (nombre del chat)</li>
    <li>Return: user_id</li>
</ul>
<pre><code>/chat/[chat_id]/addmessage</code></pre>
<p>Permite añadir un mensaje a un chat:</p>
<ul>
    <li>Method: POST</li>
    <li>Param: user_id (usuario que escribe el mensaje)</li>
    <li>Param: chat_id (chat en el que escribe el mensaje</li>
    <li>Param: text (texto del mensaje</li>   
    <li>Return: message_id</li>
</ul>
<pre><code>/chat/[chat_id]/adduser</code></pre>
<p>Permite añadir un usuario a un chat:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: chat_id (chat al que se unirá)</li>
    <li>Param: user_id (user que se unirá)</li>
    <li>Return: chat_id</li>
</ul>
<pre><code>/chat/[chat_id]/messages</code></pre>
<p>Devuelve los mensajes de un chat:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: chat_id (chat del que queremos los mensajes)</li>
    <li>Return: json con la posición de mensaje en el chat como clave y un lista con el nombre de usuario y el texto del mensaje como valor</li>
</ul>
<pre><code>/chat/[user_id]/list</code></pre>
<p>Devuelve la lista de chats de un usuario:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: user_id (usuario que queremos los mensajes)</li>
    ats_dicts[str(chat_temp["_id"])] = chat_temp["name"]
    <li>Return: json {"chat_id": "chat_name"}</li>
</ul>
<pre><code>/user/[user_id]</code></pre>
<p>Devuelve el nombre de un usuario:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: user_id (id del usuario del que queremos nombre)</li>
    <li>Return: user_name</li>
</ul>
<pre><code>/username/[username]</code></pre>
<p>Devuelve el id de un usuario:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: username (nombre del usuario del que queremos su id)</li>
    <li>Return: user_id</li>
</ul>
<pre><code>/chat/[chat_id]</code></pre>
<p>Devuelve el nombre de un chat:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: chat_id (id del chat del que queremos su nombre)</li>
    <li>Return: chat_name</li>
</ul>
<pre><code>/chats</code></pre>
<p>Devuelve todos los chats de la base de datos:</p>
<ul>
    <li>Method: GET</li>
    <li>Return: lista con los ids de los chats</li>
</ul>
<pre><code>/users</code></pre>
<p>Devuelve todos los users de la base de datos:</p>
<ul>
    <li>Method: GET</li>
    <li>Return: lista con los ids de los users</li>
</ul>
<pre><code>/user/[user_id]/messages</code></pre>
<p>Devuelve todos los mensajes de un user:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: user_id (id del user del que queremos sus mensajes)</li>
    <li>Return: json con los textos de los mensajes</li>
</ul>
<pre><code>/user/[user_name]/chats/sentiment'</code></pre>
<p>Devuelve todos los mejores chats para un user en función del sentimiento de los mensajes:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: user_name (nombre del user del que queremos los mejores chats)</li>
    <li>Return: json con los nombres y los ids de los 5 mejores chats</li>
</ul>
<pre><code>/chat/[chat_name]/similarity</code></pre>
<p>Devuelve para chat_name los chats más parecidos en función del contenido de ambos:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: chat_name (nombre del chat del que queremos los chats más parecidos)</li>
    <li>Return: json con los nombres y los ids de los 5 mejoers chats</li>
</ul>
<pre><code>/user/[user_name]/similarity</code></pre>
<p>Devuelve para user_name los users más parecidos en función del contenido de sus mensajes:</p>
<ul>
    <li>Method: GET</li>
    <li>Param: user_name (nombre del chat del que queremos los chats más parecidos)</li>
    <li>Return: lista con los nombres de los 5 users más parecidos</li>
</ul>

## Colecciones de Mongo

<p>Adjunto capturas de las colecciones</p>
<p>user</p>

![User](img/user.png)
<p>chat</p>

![Chat](img/chat.png)
<p>message:</p>

![Message](img/message.png)