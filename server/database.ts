
import {Database} from "bun:sqlite"

const db = new Database("_dragon.sqlite", {create: true})

db.run(`CREATE TABLE IF NOT EXISTS warrior(username TEXT PRIMARY KEY, easy INT DEFAULT 0, medium Int DEFAULT 0, hard INT DEFAULT 0) WITHOUT ROWID`)

db.close()
