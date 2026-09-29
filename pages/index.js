// pages/index.js
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import Link from 'next/link'

export async function getStaticProps() {
  const postsDir = path.join(process.cwd(), 'content')
  const filenames = fs.readdirSync(postsDir)
  const posts = filenames.map((name) => {
    const fullPath = path.join(postsDir, name)
    const fileContents = fs.readFileSync(fullPath, 'utf8')
    const { data, content } = matter(fileContents)
    return {
      slug: name.replace('.md', ''),
      title: data.title || slug,
      date: data.date,
      excerpt: content.slice(0, 200) + '...'
    }
  })
  // sort by date descending
  posts.sort((a, b) => new Date(b.date) - new Date(a.date))
  return { props: { posts } }
}

export default function Home({ posts }) {
  return (
    <div>
      <h1>Affiliate News</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.slug} style={{ marginBottom: '1rem' }}>
            <Link href={`/articles/${post.slug}`}><a>{post.title}</a></Link>
            <p>{post.excerpt}</p>
            <small>{new Date(post.date).toLocaleDateString()}</small>
          </li>
        ))}
      </ul>
    </div>
  )
}
