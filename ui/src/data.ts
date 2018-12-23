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
	time: string;
}

export interface User {
	id: string;
	name: string;
	token: string;
	groups: Array<Group>;
}

export interface Group {
	groupid: string;
	pages: object;
	colour: string;
}

