
// import db from '../database';
//

import {Database} from "bun:sqlite"


export default defineEventHandler(async (event) => {
    const db = new Database("_dragon.sqlite", {create: true})
    const warriors = db.prepare("select * from warrior")
    const w =  warriors.all()
    return w;
})