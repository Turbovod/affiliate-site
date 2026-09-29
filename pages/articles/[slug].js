// pages/articles/[slug].js
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { serialize } from 'next-mdx-remote/serialize'
import { MDXRemote } from 'next-mdx-remote'
import Layout from '../../components/Layout'
import AdBanner from '../../components/AdBanner'

export async function getStaticPaths() {
  const postsDir = path.join(process.cwd(), 'content')
  const filenames = fs.readdirSync(postsDir)
  const paths = filenames.map((name) => ({ params: { slug: name.replace('.md', '') } }))
  return { paths, fallback: false }
}

export async function getStaticProps({ params }) {
  const fullPath = path.join(process.cwd(), 'content', `${params.slug}.md`)
  const source = fs.readFileSync(fullPath, 'utf8')
  const { content, data } = matter(source)
  const mdxSource = await serialize(content, {
    // you can pass remark/rehype plugins here
  })
  return { props: { source: mdxSource, frontMatter: data } }
}

export default function ArticlePage({ source, frontMatter }) {
  return (
    <Layout>
      <h1>{frontMatter.title}</h1>
      <small>{new Date(frontMatter.date).toLocaleDateString()}</small>
      <MDXRemote {...source} components={{ AdBanner }} />
    </Layout>
  )
}
