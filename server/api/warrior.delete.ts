import {Database} from "bun:sqlite";


export default defineEventHandler(async (event) => {
    const query = getQuery(event);
    if (!("username" in query)) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Missing username',
        })
    }

    const db = new Database("_dragon.sqlite", {create: true});
    const username = query["username"] as string;
    const del = db.prepare("delete from warrior where username = ?");
    del.run(username);
    return `"Done"`
})