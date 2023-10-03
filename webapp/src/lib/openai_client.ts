import { SECRET_OPENAI_API_KEY } from '$env/static/private';
import { Configuration, OpenAIApi, type ChatCompletionRequestMessage } from 'openai';

const configuration = new Configuration({
	apiKey: SECRET_OPENAI_API_KEY
});
const openai = new OpenAIApi(configuration);

export async function createChatCompletion(
	document: string[],
	question: string
): Promise<string | null> {
	let messages = [];
	let systemContent = `Eres un arquitecto de datos, ayudante de IA, eres un experto en modelos de datos y lenguaje canónico para el comercio minorista. 
		Obtendrás tus conocimientos sobre modelos de datos y lenguaje canónico para retail a partir de la siguiente información delimitada entre tres ticks o comillas simples..`;

	systemContent += '\n\n```';
	for (let i = 0; i < document.length; i++) {
		systemContent += '\n' + document[i];
	}
	systemContent +=
		'\n```\n\nEl usuario le hará preguntas sobre como construir un request y un response para un listado de atributos y entidades y usted deberá responder de manera concisa e a cuales entidades y atributos canonicos entregados como contexto se puede mapear o asiociar incluir el request y response en formato JSON..';

	messages.push({
		role: 'system',
		content: systemContent
	} satisfies ChatCompletionRequestMessage);

	let prompt = question;

	messages.push({
		role: 'user',
		content: prompt
	} satisfies ChatCompletionRequestMessage);

	console.log(messages);
	try {
		let response = await openai.createChatCompletion({
			model: 'gpt-3.5-turbo-16k',
			messages: messages,
			temperature: 1,
			max_tokens: 2000
		});

		if (response.data.choices.length > 0) {
			return response.data.choices[0].message!.content;
		} else {
			return null;
		}
	} catch (error: any) {
		if (error.response) {
			console.log(error.response.status);
			console.log(error.response.data);
		} else {
			console.log(error.message);
		}
		return null;
	}
}
