import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'

export default async function ReferralRedirect({ params }: { params: { slug: string } }) {
  const supabase = createClient()

  const { data: link, error } = await supabase
    .from('referral_links')
    .select('id, target_url')
    .eq('slug', params.slug)
    .single()

  if (error || !link) {
    return <div>Link not found or expired.</div>
  }

  await supabase.rpc('increment_clicks', { row_id: link.id })

  await supabase
    .from('referral_links')
    .update({
      clicks:
        (await supabase.from('referral_links').select('clicks').eq('id', link.id).single()).data
          ?.clicks! + 1,
    })
    .eq('id', link.id)

  redirect(link.target_url)
}
