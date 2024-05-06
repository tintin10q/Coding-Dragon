
import {Database} from "bun:sqlite"

const db = new Database("_dragon.sqlite", {create: true})

db.run(`CREATE TABLE IF NOT EXISTS warrior(username TEXT PRIMARY KEY) WITHOUT ROWID`)

db.close()
