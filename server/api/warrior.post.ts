
import {Database} from "bun:sqlite"
//
import z from "zod"
import {profile} from "bun:jsc";

const leeturl = 'https://leetcode-stats-api.herokuapp.com/'

const leetresponseParser = z.object({
      status: z.literal('success'),
      totalSolved: z.number(),
      easySolved: z.number(),
      mediumSolved: z.number(),
      hardSolved: z.number()
})

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

    const response = await fetch(new URL(`/${username}`, leeturl))
    const data = await response.json()
    const profileResult = leetresponseParser.safeParse(data)

    if (profileResult.error) {
       throw createError({statusCode: 404, statusMessage: "Username not found on Leetcode :("})
    }
    const profile = profileResult.data;

    const signup = db.prepare("insert into warrior (username, easy, medium, hard) values (?, ?, ?, ?)")
    signup.run(username, profile.easySolved, profile.mediumSolved, profile.hardSolved);
    db.close();
    return {username, easy: profile?.easySolved, medium: profile.mediumSolved, hard: profile.hardSolved};
})