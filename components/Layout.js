// components/Layout.js
import Head from 'next/head'
import AdBanner from './AdBanner'

export default function Layout({ children }) {
  return (
    <>
      <Head>
        <title>Affiliate News</title>
        <meta name="description" content="Автоматический аффилиат‑сайт с ежедневными статьями" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <header style={{ padding: '1rem', background: '#f5f5f5' }}>
        <h1>Affiliate News</h1>
        <AdBanner />
      </header>
      <main style={{ maxWidth: '800px', margin: '2rem auto', padding: '0 1rem' }}>{children}</main>
      <footer style={{ textAlign: 'center', padding: '1rem', background: '#f5f5f5' }}>
        © {new Date().getFullYear()} Affiliate Site – автоматический контент
      </footer>
    </>
  )
}
