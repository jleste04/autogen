import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'
import { SubmitMetrics } from './submit-metrics'

export default async function Dashboard() {
  const supabase = createClient()
  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (!user) {
    return redirect('/login')
  }

  const { data: profile } = await supabase.from('profiles').select('*').eq('id', user.id).single()
  const { data: links } = await supabase.from('referral_links').select('*').eq('creator_id', user.id)

  const totalClicks = links?.reduce((acc, curr) => acc + curr.clicks, 0) || 0

  return (
    <div className="mx-auto max-w-4xl space-y-8 p-6">
      <header className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Welcome, {profile?.username || 'Creator'}</h1>
        <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
          Active
        </span>
      </header>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Total Link Clicks</h3>
          <p className="mt-2 text-4xl font-bold">{totalClicks}</p>
        </div>
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Est. Payout (Pending)</h3>
          <p className="mt-2 text-4xl font-bold text-gray-400">--</p>
        </div>
      </div>

      <div className="rounded-xl border bg-white p-6">
        <h2 className="mb-4 text-xl font-bold">Your Links</h2>
        <div className="space-y-2">
          {links?.map((link) => (
            <div key={link.id} className="flex justify-between rounded bg-gray-50 p-3">
              <span className="font-mono text-blue-600">westgate.com/r/{link.slug}</span>
              <span className="text-gray-600">{link.clicks} clicks</span>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-gray-50 p-6">
        <h2 className="mb-4 text-xl font-bold">Submit Weekly Metrics</h2>
        <SubmitMetrics userId={user.id} />
      </div>
    </div>
  )
}
