// import db from '../database';
//

import {Database} from "bun:sqlite"


export default defineEventHandler(async (event) => {
    const query = getQuery(event)
    if ("username" in query) {
        const username = query["username"] as string;
        const db = new Database("_dragon.sqlite", {create: true})

        const warrior = db.prepare("select * from warrior where username = ?")
        const him = warrior.all(username)
        if (!him.length) {
            throw createError({
                statusCode: 404,
                statusMessage: 'Username not found',
            })
        }
        return him[0];
    }

    const db = new Database("_dragon.sqlite", {create: true})
    const warriors = db.prepare("select * from warrior")
    const w = warriors.all()
    return w;
})