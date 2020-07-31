import type { State } from 'src/state/reducer'
import { LocaleKey, LocaleWithKey, getLocaleWithKey } from 'src/i18n/i18n'

export const selectLocaleKey = (state: State): LocaleKey => state.settings.localeKey

export const selectLocale = (state: State): LocaleWithKey => getLocaleWithKey(selectLocaleKey(state))
