'use client'

import { createClient } from '@/utils/supabase/client'
import { useState } from 'react'

export function SubmitMetrics({ userId }: { userId: string }) {
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setStatus('')

    const form = new FormData(e.currentTarget)
    const platform = form.get('platform') as string
    const views = form.get('views')
    const file = form.get('screenshot') as File

    const supabase = createClient()

    const fileExt = file.name.split('.').pop()
    const fileName = `${userId}/${Date.now()}.${fileExt}`
    const { data: fileData, error: uploadError } = await supabase.storage
      .from('screenshots')
      .upload(fileName, file)

    if (uploadError) {
      setLoading(false)
      setStatus('Error uploading screenshot.')
      return
    }

    const { error: dbError } = await supabase.from('social_metrics').insert({
      creator_id: userId,
      platform,
      views: Number(views),
      week_start_date: new Date().toISOString(),
      screenshot_url: fileData.path,
    })

    if (dbError) {
      setStatus('Error saving data.')
    } else {
      setStatus('Success! Metrics submitted.')
      ;(e.target as HTMLFormElement).reset()
    }
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <select name="platform" className="rounded border p-2">
          <option value="instagram">Instagram</option>
          <option value="tiktok">TikTok</option>
          <option value="youtube">YouTube</option>
        </select>
        <input
          name="views"
          type="number"
          placeholder="View Count"
          className="rounded border p-2"
          required
        />
      </div>
      <input
        name="screenshot"
        type="file"
        accept="image/*"
        className="block w-full text-sm text-gray-500 file:mr-4 file:rounded-full file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-blue-700 hover:file:bg-blue-100"
        required
      />

      <button
        disabled={loading}
        className="rounded bg-black px-4 py-2 text-white hover:bg-gray-800 disabled:opacity-50"
      >
        {loading ? 'Uploading...' : 'Submit Proof'}
      </button>
      {status && <p className="text-sm font-bold">{status}</p>}
    </form>
  )
}
