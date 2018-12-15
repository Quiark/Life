export interface Comment {
	ix: number;
	author: string;
	text: string;
	time: number;
}

export interface Post {
	groupid: string;
	postid: string;
	text: string;
	comments: Array<Comment>;
	time: number;
}

export interface User {
	id: string;
	name: string;
	groups: Array<Group>;
}

export interface Group {
	groupid: string;
	pages: object;
	colour: string;
}

