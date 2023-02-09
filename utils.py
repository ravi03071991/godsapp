from sentence_transformers import SentenceTransformer
import openai
import pinecone
import json
import streamlit as st

pinecone.init(api_key=st.secrets["pinecone_api_key"],
              environment=st.secrets["pinecone_environment"])

sentencemodel = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def convert_to_float(embeddings):
    embeddings_float = []
    for embed in embeddings:
        embed = list(embed)
        embed = [float(val) for val in embed]
        embeddings_float.append(embed)
    return embeddings_float

with open("finaldata.json", "r") as f:
    finaldata = json.loads(f.read())

def qa(genre, query):

    # Basic Checks
    if not query:
        return "Please enter your query."
    if not genre:
        return "Please select genre."

    query = query + " Don't make up responses. Keep the answer strictly to the text provided."

    embeddings_sen = sentencemodel.encode([query])

    index = pinecone.Index(genre)
    res = index.query(vector=convert_to_float(
        embeddings_sen), top_k=8)

    ids = [i['id'] for i in res['matches']]

    context = ''

    for id in ids:
        context = context + str(id) + ": " + finaldata[genre][str(id)] + "\n\n"

    prompt = ''

    if genre == 'bible':
        prompt = "Format:\n\nContext:\n\n4.15: The woman said to him, “Sir, give me this water, so that I don’t get thirsty, neither come all the way here to draw.”\n4.19: The woman said to him, “Sir, I perceive that you are a prophet.\n5.41: I don’t receive glory from men.\n10.27: My sheep hear my voice, and I know them, and they follow me.\n20.13: They told her, “Woman, why are you weeping?”She said to them, “Because they have taken away my Lord, and I don’t know where they have laid him.”\n4.42: They said to the woman, “Now we believe, not because of your speaking; for we have heard for ourselves, and know that this is indeed the Christ, the Savior of the world.”\n11.29: When she heard this, she arose quickly, and went to him.\n2.4: Jesus said to her,“Woman, what does that have to do with you and me? My hour has not yet come.”\n\nQuestion: How to woo woman?\n\nAnswer: t give any specific advice on \"how to woo a woman\". The Bible teaches principles of love, respect, and selflessness, and these can be applied in all aspects of life, including relationships and dating.\n\nSome verses that may offer guidance in relationships include:\n\n\"Love is patient, love is kind. It does not envy, it does not boast, it is not proud. It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs. Love does not delight in evil but rejoices with the truth. It always protects, always trusts, always hopes, always perseveres.\" \n\n\"Do to others as you would have them do to you.\" \n\n\"So God created man in his own image, in the image of God he created him; male and female he created them.\" \n\nThese verses can serve as a foundation for building healthy, loving relationships, including with romantic partners. By showing love, kindness, patience, and respect, one can form a strong bond with another person. However, it's important to remember that every individual is unique and what works for one person may not work for another. Ultimately, the best approach is to be yourself, treat others with respect, and communicate openly and honestly.\n\nFormat:\n\nContext:\n\n4.36: He who reaps receives wages, and gathers fruit to eternal life; that both he who sows and he who reaps may rejoice together.\n6.63: It is the spirit who gives life. The flesh profits nothing. The words that I speak to you are spirit, and are life.\n12.19: The Pharisees therefore said among themselves, “See how you accomplish nothing. Behold, the world has gone after him.”\n17.13: But now I come to you, and I say these things in the world, that they may have my joy made full in themselves.\n1.9: The true light that enlightens everyone was coming into the world.\n5.29: and will come out; those who have done good, to the resurrection of life; and those who have done evil, to the resurrection of judgment.\n17.22: The glory which you have given me, I have given to them; that they may be one, even as we are one;\n6.30: They said therefore to him, “What then do you do for a sign, that we may see, and believe you? What work do you do?\n\nQuestion: What is success?\n\nAnswer: In the Bible, success is often defined as living a life that is pleasing to God and fulfilling one's divine purpose. The Bible teaches that true success goes beyond temporal achievements and wealth and is instead rooted in a relationship with God and living a life of obedience to His commands.\n\nSome verses that highlight the importance of success in the Bible include:\n\n\"Trust in the Lord with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make straight your paths.\" \n\n\"So, whether you eat or drink, or whatever you do, do all to the glory of God.\" \n\n\"And we know that in all things God works for the good of those who love him, who have been called according to his purpose.\" (\n\n\"For the eyes of the Lord are on the righteous, and his ears are attentive to their prayer, but the face of the Lord is against those who do evil.\" \n\nIn conclusion, success according to the Bible is achieved by living a life that is pleasing to God, following His commands, and fulfilling one's divine purpose. It is not defined by worldly achievements or material wealth, but by a strong relationship with God and obedience to His will.\n\nFormat:\n\nContext:\n\n"
    elif genre == "quran":
        prompt = "Format:\n\nContext:\n\n4.4: And give unto women their marriage portions in the spirit of a gift; but if they, of their own accord, give up unto you aught thereof, then enjoy it with pleasure and good cheer\n60.10: O YOU who have attained to faith! Whenever believing women come unto you, forsaking the domain of evil, examine them, [although only] God is fully aware of their faith; and if you have thus ascertained that they are believers, do not send them back to the deniers of the truth, [since] they are [no longer] lawful to their erstwhile husbands, and these are [no longer] lawful to them. None the less, you shall return to them whatever they have spent [on their wives by way of dower]; and [then, O believers,] you will be committing no sin if you marry them after giving them their dowers. On the other hand, hold not to the marriage-tie with women who [continue to] deny the truth, and ask but for [the return of] whatever you have spent [by way of dower] -just as they [whose wives have gone over to you] have the right to demand [the return of] whatever they have spent. Such is God's judgment: He judges between you [in equity] - for God is all-knowing, wise\n4.34: MEN SHALL take full care of women with the bounties which God has bestowed more abundantly on the former than on the latter, and with what they may spend out of their possessions. And the righteous women are the truly devout ones, who guard the intimacy which God has [ordained to be] guarded. And as for those women whose ill-will you have reason to fear, admonish them [first]; then leave them alone in bed; then beat them; and if thereupon they pay you heed, do not seek to harm them. Behold, God is indeed most high, great\n2.231: And so, when you divorce women and they are about to reach the end of their waiting-term, then either retain them in a fair manner or let them go in a fair manner. But do not retain them against their will in order to hurt [them]: for he who does so sins indeed against himself. And do not take [these] messages of God in a frivolous spirit; and remember the blessings with which God has graced you, and all the revelation and the wisdom which He has bestowed on you from on high in order to admonish you thereby; and remain conscious of God, and know that God has full knowledge of everything\n19.20: Said she: \"How can I have a son when no man has ever touched me? - for, never have I been a loose woman\n27.23: “Behold, I found there a woman ruling over them; and she has been given [abundance] of all [good] things, and hers is a mighty throne\n2.221: AND DO NOT marry women who ascribe divinity to aught beside God ere they attain to [true] belief: for any believing bondwoman [of God] is certainly better than a woman who ascribes divinity to aught beside God, even though she please you greatly. And do not give your women in marriage to men who ascribe divinity to aught beside God ere they attain to [true] belief: for- any believing bondman [of God] is certainly better than a man who ascribes divinity to aught beside God, even though he please you greatly. [Such as] these invite unto the fire, whereas God invites unto paradise, and unto [the achievement of] forgiveness by His leave; and He makes clear His messages unto mankind, so that they might bear them in mind\n92.4: Verily, [O men,] you aim at most divergent ends\n\nQuestion: How to win over woman?\n\nAnswer: Winning someone over, regardless of gender, should not be the primary focus in relationships according to Islamic teachings. Instead, the Quran emphasizes building strong, mutual relationships based on love, compassion, trust, respect, and empathy.\n\nSome ways to cultivate these qualities in relationships include:\n\nTreating others with kindness and fairness\nBeing honest and trustworthy\nBeing a good listener and communicator\nBeing patient and understanding\nShowing gratitude and appreciation\nIt's also important to remember that the ultimate goal in any relationship should be to please Allah and seek His pleasure, and not just to please one's own desires or ego.\n\nFormat:\n\nContext:\n\n56.33: never-failing and never out of reach\n23.61: it is they who vie with one another in doing good works, and it is they who outrun [all others] in attaining to them\n18.92: And once again he chose the right means (to achieve a right end)\n31.5: It is they who follow the guidance [that comes to them] from their Sustainer; and it is they, they who shall attain to a happy state\n87.17: although the life to come is better and more enduring\n19.76: And God endows those who avail themselves of [His] guidance with an ever-deeper consciousness of the right way; and good deeds, the fruit whereof endures forever, are, in thy Sustainer's sight, of far greater merit [than any worldly goods], and yield far better returns\n9.112: [It is a triumph of] those who turn [unto God] in repentance [whenever they have sinned], and who worship and praise [Him], and go on and on [seeking His goodly acceptance], and bow down [before Him] and prostrate themselves in adoration, and enjoin the doing of what is right and forbid the doing of what is wrong, and keep to the bounds set by God. And give thou [O Prophet] the glad tiding [of God's promise] to all believers\n18.89: And once again he chose the right means [to achieve a right end]\n\nQuestion: What is success?\n\nAnswer: In Islam, success is defined as achieving the pleasure of Allah and following His commandments. The Quran states that success can be attained through obedience to Allah and doing good deeds, such as helping those in need, being honest, and maintaining justice.\n\nAnother aspect of success in Islam is gaining nearness to Allah through worship, devotion, and mindfulness of Him. The Quran mentions that true success comes from attaining salvation in the afterlife and being granted entry into paradise.\n\nAdditionally, success in this life can also be defined as having financial stability, a strong family, and good health, as long as these blessings are used in accordance with Allah's commandments and for the benefit of others. In other words, material success is valued in Islam, but it must be balanced with spiritual success and used for the greater good.\n\nFormat:\n\nContext:\n\n"
    elif genre == "gita":
        prompt = "Format:\n\nContext:\n\n4.42: Therefore, with the sword of knowledge, cut asunder the doubts that have arisen in your heart. O scion of Bharat, establish yourself in karm yog. Arise, stand up, and take action!\n4.34: Learn the Truth by approaching a spiritual master. Inquire from him with reverence and render service unto him. Such an enlightened Saint can impart knowledge unto you because he has seen the Truth.\n8.7: Therefore, always remember Me and also do your duty of fighting the war. With mind and intellect surrendered to Me, you will definitely attain Me; of this, there is no doubt.\n18.6: These activities must be performed without attachment and expectation for rewards. This is My definite and supreme verdict, O Arjun.\n18.4: Now hear My conclusion on the subject of renunciation, O tiger amongst men, for renunciation has been declared to be of three kinds.\n4.15: Knowing this truth, even seekers of liberation in ancient times performed actions. Therefore, following the footsteps of those ancient sages, you too should perform your duty.\n4.12: In this world, those desiring success in material activities worship the celestial gods, since material rewards manifest quickly.\n4.16: What is action and what is inaction? Even the wise are confused in determining this. Now I shall explain to you the secret of action, by knowing which, you may free yourself from material bondage.\n\nQuestion: how to woo woman?\n\nAnswer: The Bhagavad Gita does not provide specific advice on how to woo a woman. It is a text that focuses on the path to self-realization and offers teachings on dharma, yoga, and devotion. The text emphasizes inner transformation and development of spiritual wisdom, rather than offering advice on interpersonal relationships or romance.\n\nFormat:\n\nContext:\n\n4.22: Content with whatever gain comes of its own accord, and free from envy, they are beyond the dualities of life. Being equipoised in success and failure, they are not bound by their actions, even while performing all kinds of activities.\n4.12: In this world, those desiring success in material activities worship the celestial gods, since material rewards manifest quickly.\n14.24 - 14.25: Those who are alike in happiness and distress; who are established in the self; who look upon a clod, a stone, and a piece of gold as of equal value; who remain the same amidst pleasant and unpleasant events; who are intelligent; who accept both blame and praise with equanimity; who remain the same in honor and dishonor; who treat both friend and foe alike; and who have abandoned all enterprises – they are said to have risen above the three guṇas.\n14.10: Sometimes goodness (sattva) prevails over passion (rajas) and ignorance (tamas), O scion of Bharat. Sometimes passion (rajas) dominates goodness (sattva) and ignorance (tamas), and at other times ignorance (tamas) overcomes goodness (sattva) and passion (rajas).\n18.12: The three-fold fruits of actions—pleasant, unpleasant, and mixed—accrue even after death to those who are attached to personal reward. But, for those who renounce the fruits of their actions, there are no such results in the here or hereafter.\n14.16: It is said the fruit of actions performed in the mode of goodness bestow pure results. Actions done in the mode of passion result in pain, while those performed in the mode of ignorance result in darkness.\n18.2: The Supreme Divine Personality said: Giving up of actions motivated by desire is what the wise understand as sanyās. Relinquishing the fruits of all actions is what the learned declare to be tyāg.\n8.21: That unmanifest dimension is the supreme goal, and upon reaching it, one never returns to this mortal world. That is My Supreme Abode.\n\nQuestion: What is success?\n\nAnswer: The Bhagavad Gita defines success as performing one's duties and responsibilities in life to the best of one's abilities, without attachment to the fruits of one's actions and remaining steadfast in the face of success or failure. According to the Gita, true success lies in doing one's duty selflessly and dedicating the outcome to God.\n\nFormat:\n\nContext:\n\n"

    prompt = prompt + context + "Question: " + query + "\n" + "Answer:\n\n"

    openai.api_key = st.secrets["openai_apikey"]

    # query = query + "Keep your answer strictly to context provided. If you are not confident about answer mention as I am not confident of answer"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response["choices"][0]["text"] + "----------------" + context
