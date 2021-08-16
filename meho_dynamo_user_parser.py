# import
import json
import codecs 
import subprocess


def main():

  with open('user_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'User-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download User ready!")
  with codecs.open('./user_dump.json','r', 'utf-8') as f_r:
    users_dump = json.load(f_r)

  all_users = []
  rawUsers = users_dump['Items']
  count = 0
  for userRaw in rawUsers:
    count = count + 1
    user = dict({})
    user["user_id"] = userRaw['id']['S']
    user["user_email"] = userRaw['email']['S']
    user["user_nickname"] = userRaw['username']['S']
    user["user_created_date"] = userRaw['createdAt']['S']

    user["user_profession"] = None if userRaw.get('profession') is None else userRaw['profession'].get('S')
    user["user_goals_flatten"] = None if userRaw.get('goals') is None else flattenListString(userRaw['goals'].get('L'))
    user["user_interests_flatten"] = None if userRaw.get('interests') is None else flattenListString(userRaw['interests'].get('L'))

    all_users.append(user)

    

  f_r.close()
  print("Total users:" + str(count))

  # write to file
  with codecs.open('all_user.json', 'w', encoding='utf-8') as f_w:
    json.dump(all_users, f_w, indent = 4, ensure_ascii=False)
      

  # clean ups
  f_w.close()



def flattenListString(item_list):
  if item_list is None:
    return None

  flattenedString = ""
  for item in item_list:
    flattenedString = flattenedString + item["S"] + ";"

  return flattenedString


if __name__ == "__main__":
    main()
