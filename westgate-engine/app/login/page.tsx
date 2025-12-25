import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'
import { headers } from 'next/headers'

export default function Login({ searchParams }: { searchParams: { message: string } }) {
  const signIn = async (formData: FormData) => {
    'use server'
    const email = formData.get('email') as string
    const supabase = createClient()
    const origin = headers().get('origin')

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        shouldCreateUser: false,
        emailRedirectTo: `${origin}/auth/callback`,
      },
    })

    if (error) {
      return redirect('/login?message=Could not authenticate user')
    }

    return redirect('/login?message=Check your email for the magic link')
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <form action={signIn} className="w-full max-w-md space-y-4 rounded-lg bg-white p-8 shadow">
        <h1 className="text-center text-2xl font-bold">Creator Portal</h1>
        <input
          name="email"
          placeholder="you@westgate.com"
          required
          className="w-full rounded border p-2"
        />
        <button className="w-full rounded bg-blue-600 p-2 text-white">Send Magic Link</button>
        {searchParams?.message && (
          <p className="text-center text-sm text-red-500">{searchParams.message}</p>
        )}
      </form>
    </div>
  )
}
