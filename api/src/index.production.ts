import '../config/dotenv'

import 'reflect-metadata'

import Server from './server/Server'

const server = new Server()
server.listen()

process.on('beforeExit', () => server.close())
