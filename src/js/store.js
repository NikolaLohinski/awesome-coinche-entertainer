export default {
  mutations: {
    language (state, language) {
      state.i18n.locale = language;
      localStorage['language'] = language;
    }
  },
  getters: {
    language (state) {
      return state.i18n.locale;
    },
    languages (state) {
      const languages = [];
      for (const language in state.i18n.translations) {
        if (!state.i18n.translations.hasOwnProperty(language)) continue;
        languages.push(language);
      }
      return languages;
    }
  }
};

