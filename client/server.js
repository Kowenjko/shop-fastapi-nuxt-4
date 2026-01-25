import { createServer } from 'http'
import { loadNuxt } from 'nuxt'

async function start() {
  const nuxt = await loadNuxt({ dev: false, rootDir: process.cwd() })
  const server = createServer(nuxt.render)

  const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000
  const host = process.env.HOST || '0.0.0.0'

  server.listen(port, host, () => {
    console.log(`Nuxt SSR listening on ${host}:${port}`)
  })
}

start()
