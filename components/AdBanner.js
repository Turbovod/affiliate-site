// components/AdBanner.js
import Image from 'next/image'

export default function AdBanner() {
  // Simple placeholder banner – replace src with real ad code later
  return (
    <div style={{ textAlign: 'center', margin: '1rem 0' }}>
      <Image src="/ads/banner1.png" alt="Ad banner" width={728} height={90} />
    </div>
  )
}
