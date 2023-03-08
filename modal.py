import modal

app_image = modal.Image.debian_slim().pip_install(
    "pinecone-client",
    "openai",
)

stub = modal.Stub("askholybot", image=app_image)

stub.sv = modal.SharedVolume()

if stub.is_inside():
    import json
    import os
    import pinecone
    import openai

    pinecone_api_key = "9554fd78-b53b-48e4-90fa-dfcd786ebb0c"
    pinecone_environment = "us-east1-gcp"
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

@stub.function(
    timeout=12000,
    secret=modal.Secret.from_name("ASK-HOLY"),
    mounts=[
        modal.Mount.from_local_file(
            "./finaldata.json", remote_path="/askholy/finaldata.json"
        )
    ],
)
def get_response(genre, query):
    # Basic Checks
    if not query:
        return "Please enter your query."
    if not genre:
        return "Please select genre."

    import json

    file_path = "/askholy/finaldata.json"

    with open(file_path, "r") as f:
        finaldata = json.loads(f.read())

    openai.api_key = os.environ["OPEN_AI_API_KEY"]

    response = openai.Embedding.create(input=[query], model="text-embedding-ada-002")
    embedding = response["data"][0]["embedding"]

    index = pinecone.Index(genre)

    res = index.query(vector=(embedding), top_k=8)

    ids = [i["id"] for i in res["matches"]]

    context = ""

    for id in ids:
        context = context + str(id) + ": " + finaldata[genre][str(id)] + "\n\n"

    prompt = ""

    if genre == "bible":
        prompt = "Format:\n\nContext:\n\n4.36: He who reaps receives wages, and gathers fruit to eternal life; that both he who sows and he who reaps may rejoice together.\n7.18: He who speaks from himself seeks his own glory, but he who seeks the glory of him who sent him is true, and no unrighteousness is in him.\n12.25: He who loves his life will lose it. He who hates his life in this world will keep it to eternal life.\n13.17: If you know these things, blessed are you if you do them.\n4.37: For in this the saying is true, ‘One sows, and another reaps.’\n15.8: “In this is my Father glorified, that you bear much fruit; and so you will be my disciples.\n6.63: It is the spirit who gives life. The flesh profits nothing. The words that I speak to you are spirit, and are life.\n12.24: Most certainly I tell you, unless a grain of wheat falls into the earth and dies, it remains by itself alone. But if it dies, it bears much fruit.\n\nQuestion: What is success?\n\nAnswer: The Bible does not provide a specific definition of success, but it offers guidance on how to live a fulfilling and purposeful life. Success is often associated with a person's relationship with God and their obedience to His commandments. True success is not measured by worldly achievements or possessions, but by one's character, integrity, and impact on the lives of others. Ultimately, success is about fulfilling God's purposes, serving others, and making a positive difference in the world.\n\nFormat:\n\nContext:\n\n20.15: Jesus said to her,“Woman, why are you weeping? Who are you looking for?”She, supposing him to be the gardener, said to him, “Sir, if you have carried him away, tell me where you have laid him, and I will take him away.”\n4.28: So the woman left her water pot, and went away into the city, and said to the people,\n4.16: Jesus said to her,“Go, call your husband, and come here.”\n14.15: If you love me, keep my commandments.\n8.5: Now in our law, Moses commanded us to stone such women. What then do you say about her?”\n4.15: The woman said to him, “Sir, give me this water, so that I don’t get thirsty, neither come all the way here to draw.”\n4.11: The woman said to him, “Sir, you have nothing to draw with, and the well is deep. So where do you get that living water?\n2.5: His mother said to the servants, “Whatever he says to you, do it.”\n\nQuestion: How to woo woman?\n\nAnswer: The Bible does not provide specific instructions on how to \"woo\" or court a woman, but it does offer general principles on how to approach relationships with respect and honor. Men should treat women with kindness, respect, and dignity, and seek to develop a deep and meaningful relationship based on mutual trust and respect. They should practice humility and selflessness, demonstrate love and compassion, and seek to honor God in their relationships. Ultimately, successful relationships are built on a foundation of mutual love, trust, and commitment, and guided by biblical principles of purity, faithfulness, and service to others.\n\nFormat:\n\nContext:\n\n"
    elif genre == "quran":
        prompt = 'Format:\n\nContext:\n\n16.30: But [when] those who are conscious of God are asked, "What is it that your Sustainer has bestowed from on high?" -they answer, "Goodness supreme!" Good fortune awaits, in this world, all who persevere in doing good; but their ultimate state will be far better still: for, how excellent indeed will be the state of the God-conscious [in the life to come]\n44.57: an act of thy Sustainer’s favour: and that, that will be the triumph supreme\n110.1: WHEN GOD\'S SUCCOUR comes, and victory\n101.7: shall find himself in a happy\' state of life\n37.60: Verily, this - this indeed - is the triumph supreme!”\n88.9: well-pleased with [the fruit of] their striving\n53.39: and that nought shall be accounted unto man but what he is striving for\n87.17: although the life to come is better and more enduring\n\nQuestion: What is success?\n\nAnswer: The Quran defines success as attaining Allah\'s pleasure and earning a place in paradise. This can be achieved through faith in Allah, performing good deeds, and following the guidance of the Prophet Muhammad. Success in the worldly sense, such as wealth and power, is temporary and secondary to spiritual success. True success is ultimately determined by Allah and depends on one\'s sincerity and obedience to His commands.\n\nFormat:\n\nContext:\n\n33.32: O wives of the Prophet! You are not like any of the [other] women, provided that you remain [truly] conscious of God. Hence, be not over-soft in your speech, lest any whose heart is diseased should be moved to desire [you]: but, withal, speak in a kindly way\n4.4: And give unto women their marriage portions in the spirit of a gift; but if they, of their own accord, give up unto you aught thereof, then enjoy it with pleasure and good cheer\n2.223: Your wives are your tilth; go, then, unto your tilth as you may desire, but first provide something for your souls, and remain conscious of God, and know that you are destined to meet Him. And give glad tidings unto those who believe\n2.235: But you will incur no sin if you give a hint of [an intended] marriage-offer to [any of] these women, or if you conceive such an intention without making it obvious: [for] God knows that you intend to ask them in marriage. Do not, however, plight your troth with them in secret, but speak only in a decent manner; and do not proceed with tying the marriage-knot ere the ordained [term of waiting] has come to its end. And know that God knows what is in your minds, and therefore remain conscious of Him; and know, too, that God is much-forgiving, forbearing\n2.221: AND DO NOT marry women who ascribe divinity to aught beside God ere they attain to [true] belief: for any believing bondwoman [of God] is certainly better than a woman who ascribes divinity to aught beside God, even though she please you greatly. And do not give your women in marriage to men who ascribe divinity to aught beside God ere they attain to [true] belief: for- any believing bondman [of God] is certainly better than a man who ascribes divinity to aught beside God, even though he please you greatly. [Such as] these invite unto the fire, whereas God invites unto paradise, and unto [the achievement of] forgiveness by His leave; and He makes clear His messages unto mankind, so that they might bear them in mind\n33.59: O Prophet! Tell thy wives and thy daughters, as well as all [other] believing women, that they should draw over themselves some of their outer garments [when in public]: this will be more conducive to their being recognized [as decent women] and not annoyed. But [withal,] God is indeed much- forgiving, a dispenser of grace\n17.64: Entice, then, with thy voice such of them as thou canst, and bear upon them with all thy horses and all thy men, and be their partner in [all sins relating to] worldly goods and children, and hold out [all manner of] promises to them: and [they will not know that] whatever Satan promises them is but meant to delude the mind\n2.222: AND THEY will ask thee about [woman\'s] monthly courses. Say: "It is a vulnerable condition. Keep, therefore, aloof from women during their monthly courses, and do not draw near unto them until they are cleansed; and when they are cleansed, go in unto them as God has bidden you to do." Verily, God loves those who turn unto Him in repentance and He loves those who keep themselves pure\n\nQuestion: How to woo woman?\n\nAnswer: The Quran emphasizes the importance of treating women with respect, kindness, and compassion, and following Islamic principles of modesty and propriety. Men should seek to develop a deep and meaningful relationship with a woman based on mutual respect, trust, and the intention of marriage. Courtship should be conducted in a halal (permissible) manner, guided by Islamic principles, and with the involvement of families if possible. Ultimately, a successful relationship is one that is built on a foundation of mutual love, respect, and commitment, and that is guided by Quranic values and principles.\n\nFormat:\n\nContext:\n\n'
    elif genre == "gita":
        prompt = "Format:\n\nContext:\n4.22: Content with whatever gain comes of its own accord, and free from envy, they are beyond the dualities of life. Being equipoised in success and failure, they are not bound by their actions, even while performing all kinds of activities.\n18.26: The performer is said to be in the mode of goodness, when he or she is free from egotism and attachment, endowed with enthusiasm and determination, and equipoised in success and failure.\n6.6: For those who have conquered the mind, it is their friend. For those who have failed to do so, the mind works like an enemy.\n6.37: Arjun said: What is the fate of the unsuccessful yogi who begins the path with faith, but who does not endeavor sufficiently due to an unsteady mind and is unable to reach the goal of Yog in this life?\n4.12: In this world, those desiring success in material activities worship the celestial gods, since material rewards manifest quickly.\n2.48: Be steadfast in the performance of your duty, O Arjun, abandoning attachment to success and failure. Such equanimity is called Yog.\n14.24 - 14.25: Those who are alike in happiness and distress; who are established in the self; who look upon a clod, a stone, and a piece of gold as of equal value; who remain the same amidst pleasant and unpleasant events; who are intelligent; who accept both blame and praise with equanimity; who remain the same in honor and dishonor; who treat both friend and foe alike; and who have abandoned all enterprises – they are said to have risen above the three guṇas.\n3.20 - 3.21: By performing their prescribed duties, King Janak and others attained perfection. You should also perform your duties to set an example for the good of the world. Whatever actions great persons perform, common people follow. Whatever standards they set, all the world pursues\n\nQuestion: What is success?\n\nAnswer: The Bhagavad Gita describes success as the attainment of one's true nature and purpose, which is to realize our oneness with the ultimate reality, or Brahman. This realization is achieved through selfless action, devotion to God, and detachment from the fruits of our actions. True success, therefore, is not measured by external achievements or material possessions, but by one's spiritual progress and inner fulfillment.\n\nFormat:\n\nContext:\n18.65: Always think of Me, be devoted to Me, worship Me, and offer obeisance to Me. Doing so, you will certainly come to Me. This is My pledge to you, for you are very dear to Me.\n9.34: Always think of Me, be devoted to Me, worship Me, and offer obeisance to Me. Having dedicated your mind and body to Me, you will certainly come to Me.\n9.27: Whatever you do, whatever you eat, whatever you offer as oblation to the sacred fire, whatever you bestow as a gift, and whatever austerities you perform, O son of Kunti, do them as an offering to Me.\n4.42: Therefore, with the sword of knowledge, cut asunder the doubts that have arisen in your heart. O scion of Bharat, establish yourself in karm yog. Arise, stand up, and take action!\n3.9: Work must be done as a yajna to the Supreme Lord; otherwise, work causes bondage in this material world. Therefore, O son of Kunti, for the satisfaction of God, perform your prescribed duties, without being attached to the results.\n9.31: Quickly they become virtuous, and attain lasting peace. O son of Kunti, declare it boldly that no devotee of Mine is ever lost.\n3.43: Thus knowing the soul to be superior to the material intellect, O mighty armed Arjun, subdue the lower self (senses, mind, and intellect) by the higher self (strength of the soul), and kill this formidable enemy called lust.\n2.37: If you fight, you will either be slain on the battlefield and go to the celestial abodes, or you will gain victory and enjoy the kingdom on earth. Therefore arise with determination, O son of Kunti, and be prepared to fight.\n\nQuestion: How to woo woman?\n\nAnswer: The Bhagavad Gita is a spiritual text and does not offer specific guidance on how to woo a woman. However, it emphasizes the importance of treating all beings with respect, kindness, and compassion. It also stresses the value of cultivating virtues such as humility, sincerity, and honesty, which can help create deeper and more meaningful relationships. Ultimately, the path of love and devotion to God can help us develop a pure and selfless love that transcends physical attraction and personal desires.\n\nFormat:\n\nContext:\n\n"

    query = (
        query
        + f"Don't make up an answer. Restrict your answer to the text provided from {genre}"
    )

    prompt = prompt + context + "Question: " + query + "\n" + "Answer:\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response["choices"][0]["text"] + "----------------" + context

@stub.webhook
def test(genre: str, query: str):
    try:
        response = get_response.call(genre, query)
        return response
    except Exception as e:
        print(e)
