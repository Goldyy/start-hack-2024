'use server'

import { revalidateTag } from 'next/cache'
import {OvoHunter} from '../../interfaces/ovo-hunter'
const PATH = '/api/ovo-hunters_starthack/ovo-hunters'

export async function getOvoHunters() {
    try {
        console.log('fetching data')
        const URL = 'http://backend:9081/backend'+PATH
        console.log('URL:' + URL)
        const res = await fetch(URL, {next: {tags: ['ovo-hunters']}})

        console.log(res)

        if (!res.ok) {

            throw new Error('Failed to fetch data')
        }
        const data: OvoHunter[] = await res.json()
        return data
    } catch (error) {
        console.error(error)
    }
}

export async function deleteOvoHunter(id: number) {
    try {
        const res = await fetch('http://backend:9081/backend'+PATH+'/'+id, {
            method: 'DELETE'
        })

        if (!res.ok) {
            throw new Error('Failed to delete data')
        }
    } catch (error) {
        console.error(error)
    }

    revalidateTag('ovo-hunters')
}

export async function addOvoHunter(ovoHunter: OvoHunter) {
    try {
        const res = await fetch('http://backend:9081/backend'+PATH, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(ovoHunter)
        })

        if (!res.ok) {
            throw new Error('Failed to add data')
        }
    } catch (error) {
        console.error(error)
        throw error
    }

    revalidateTag('ovo-hunters')
}