import utilities
import random

def parse_story(file_name):
        text = open(file_name, 'r')
        text_string = text.read()
        text_string = "".join(i for i in text_string if i not in utilities.BAD_CHARS)
        text_string = text_string.lower()
        punc = [" "+utilities.VALID_PUNCTUATION[i]+" " for i in range(0, len(utilities.VALID_PUNCTUATION))]
        text_string = "".join([punc[utilities.VALID_PUNCTUATION.index(text_string[i])] if text_string[i] in utilities.VALID_PUNCTUATION else text_string[i] for i in range(0, len(text_string))])
        output = text_string.split()
        text.close()
        return output

def get_prob_from_counts(counts):
        return [(i / float(sum(counts))) for i in counts]

def build_ngram_counts(words, n):
        d = {}
        for i in range(0, len(words)-n):
                key = tuple(words[i:i+n])
                new_val = words[i+n]
                if(key in d.keys()):
                        val = d.get(key)
                        if(new_val in val[0]):
                                val[1][val[0].index(new_val)] += 1
                                d.update({key: val})
                        else:
                                val[0].append(new_val)
                                val[1].extend([1])
                                d.update({key: val})
                else:
                        d.update({key: [[new_val], [1]]})
        return d

def prune_ngram_counts(counts, prune_len):
        d = {}
        for key in counts:
                val = counts.get(key)
                count_list = list(val[1][:])
                combined_list = list(zip(val[1][:], val[0][:]))
                combined_list.sort(reverse = True)
                count_list.sort(reverse = True)
                new_val = [[], []]
                j = 0
                i = 0
                while (j < len(count_list) and i < prune_len):
                        if(j < len(count_list) - 1 and count_list[j+1] == count_list[j] and i+1 == prune_len):
                                i-=1
                        new_val[0].append(combined_list[j][1])
                        new_val[1].append(combined_list[j][0])

                        i += 1
                        j += 1
                d.update({key: new_val})
        return d

def probify_ngram_counts(counts):
        d = {}
        for key in counts:
                val = counts.get(key)
                val[1] = get_prob_from_counts(val[1])
                d.update({key: val})
        return d

def build_ngram_model(words, n):
    ngram = build_ngram_counts(words, n)
    ngram = prune_ngram_counts(ngram, 15)
    return probify_ngram_counts(ngram)

def gen_bot_list(ngram_model, seed, num_tokens = 0):
        output_string = []
        curr = seed

        for word in curr:
                output_string.append(word)

        if num_tokens == 0:
                return []
        elif len(output_string) >= num_tokens:
                output_string = output_string[-(num_tokens):]
        else:
                while (len(output_string) < num_tokens):
                        token = utilities.gen_next_token(tuple(output_string[-len(curr):]), ngram_model)
                        output_string.append(token)
        return output_string

def gen_bot_text(token_list):
        output_string = ""
        punc = utilities.VALID_PUNCTUATION
        end_punc = utilities.END_OF_SENTENCE_PUNCTUATION
        cap = utilities.ALWAYS_CAPITALIZE
        for i in range(0, len(cap)):
                cap[i] = cap[i].lower()

        token_list[0] = token_list[0].capitalize()
        output_string += token_list[0]+" "

        for i in range(1, len(token_list)):
                if(token_list[i-1] in end_punc or (token_list[i]) in cap):
                        token_list[i] = token_list[i].title()
                output_string = output_string + token_list[i]
                if(i < len(token_list)-1 and not (token_list[i+1] in punc)):
                        output_string = output_string + " "

        return output_string

if __name__ == "__main__":
        
        word_list = parse_story("18155.txt")
        ngram = build_ngram_model(word_list, 30)
        token_list = gen_bot_list(ngram, utilities.gen_seed(ngram), 20)
        print(gen_bot_text(token_list))
        