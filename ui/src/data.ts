export interface Comment {
	author: string;
	text: string;
	time: string;
}

export interface Post {
	groupid: string;
	postid: string;
	text: string;
	comments: Array<Comment>;
	format: string;
	time: string;
}

export interface User {
	id: string;
	name: string;
	token: string;
	groups: Array<string>;
}

export interface Group {
	groupid: string;
	name: string;
	pages: object;
	colour: string;
}

export interface PostPayload {
	groupid: string;
	text: string;
}

