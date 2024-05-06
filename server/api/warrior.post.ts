
import {Database} from "bun:sqlite"
//


export default defineEventHandler(async (event) => {
    const db = new Database("_dragon.sqlite", {create: true})
    const query = getQuery(event)
    if (!("username" in query)) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Missing username',
        })
    }

    const username = query["username"] as string;
    const signup = db.prepare("insert into warrior (username) values (?)")
    signup.run(username);
    db.close();
    return username
})